/**
 * NexWave Tech — AI quote proxy.
 * Browser calls this Worker; the Worker holds the OpenRouter key.
 * ponytail: KV-free fixed-window rate limit per IP (resets on isolate churn).
 *           Swap to Durable Object / KV counter when abuse shows up in logs.
 */

const ALLOWED_ORIGINS = [
  'https://www.nexwave-tech.my.id',
  'https://nexwave-tech.my.id',
];
const DEV_ORIGIN = /^http:\/\/(127\.0\.0\.1|localhost):\d+$/;

const MODEL = 'deepseek/deepseek-chat';
const MAX_PROMPT = 2000;
const WINDOW_MS = 60_000;
const MAX_REQ_PER_WINDOW = 6;

const hits = new Map(); // ip -> { n, resetAt }

function allowOrigin(origin) {
  if (!origin) return null;
  if (ALLOWED_ORIGINS.includes(origin)) return origin;
  if (DEV_ORIGIN.test(origin)) return origin;
  return null;
}

function cors(origin) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    Vary: 'Origin',
  };
}

function json(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...(origin ? cors(origin) : {}) },
  });
}

function rateLimited(ip) {
  const now = Date.now();
  const rec = hits.get(ip);
  if (!rec || now > rec.resetAt) {
    hits.set(ip, { n: 1, resetAt: now + WINDOW_MS });
    if (hits.size > 5000) for (const [k, v] of hits) if (now > v.resetAt) hits.delete(k);
    return false;
  }
  rec.n += 1;
  return rec.n > MAX_REQ_PER_WINDOW;
}

function systemPrompt(lang) {
  const id = lang === 'id';
  const reject = id
    ? 'Maaf, AI ini khusus dirancang untuk mengestimasi proyek software, web, dan sistem aplikasi.'
    : 'Sorry, this AI is specifically designed for software, web, and app project estimations.';
  const L = id ? 'Indonesian' : 'English';
  return `You are Nexy, an intelligent software architecture consultant for NexWave Tech.
Your ONLY job is to analyze software/web/app project requests and return a JSON estimate.

GUARDRAIL RULES:
1. If the request is completely OUT OF TOPIC (general knowledge, politics, jokes, personal advice), return JSON:
   { "isValid": false, "rejectReason": "${reject}" }

2. If valid (any app/web/software/IT request, or empty description), return JSON:
   {
     "isValid": true,
     "title": "Short solution title in ${L}",
     "timeline": "Timeline in ${L} (e.g. 2 - 3 ${id ? 'Minggu' : 'Weeks'})",
     "techStack": "Recommended tech stack (e.g. Next.js 15, PostgreSQL, Tailwind)",
     "features": ["Feature 1 in ${L}", "Feature 2", "Feature 3"]
   }
ONLY return raw JSON. No markdown code fences.`;
}

export default {
  async fetch(request, env) {
    const origin = allowOrigin(request.headers.get('Origin'));

    if (request.method === 'OPTIONS') {
      return origin
        ? new Response(null, { status: 204, headers: cors(origin) })
        : new Response('Forbidden', { status: 403 });
    }
    if (request.method !== 'POST') return json({ error: 'Method not allowed' }, 405, origin);
    if (!origin) return json({ error: 'Origin not allowed' }, 403, null);

    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    if (rateLimited(ip)) {
      return json({ error: 'Too many requests. Please wait a minute.' }, 429, origin);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ error: 'Invalid JSON body' }, 400, origin);
    }

    const prompt = String(body.prompt ?? '').slice(0, MAX_PROMPT);
    const lang = body.lang === 'id' ? 'id' : 'en';

    if (!env.OPENROUTER_API_KEY) {
      return json({ error: 'Service not configured' }, 503, origin);
    }

    let upstream;
    try {
      upstream = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${env.OPENROUTER_API_KEY}`,
          'Content-Type': 'application/json',
          'HTTP-Referer': 'https://www.nexwave-tech.my.id',
          'X-Title': 'NexWave Tech Quote Calculator',
        },
        body: JSON.stringify({
          model: MODEL,
          max_tokens: 300,
          messages: [
            { role: 'system', content: systemPrompt(lang) },
            {
              role: 'user',
              content: prompt || 'Selected category: Custom Application / Web System, Industry: Business & IT Services',
            },
          ],
        }),
      });
    } catch {
      return json({ error: 'AI engine unreachable' }, 502, origin);
    }

    if (!upstream.ok) {
      // Never surface upstream body: it can echo key/account details.
      return json({ error: 'AI engine error', status: upstream.status }, 502, origin);
    }

    const data = await upstream.json();
    const raw = data?.choices?.[0]?.message?.content;
    if (typeof raw !== 'string') return json({ error: 'Empty AI response' }, 502, origin);

    let parsed;
    try {
      parsed = JSON.parse(raw.replace(/```json/g, '').replace(/```/g, '').trim());
    } catch {
      return json({ error: 'AI returned malformed JSON' }, 502, origin);
    }

    return json(parsed, 200, origin);
  },
};
