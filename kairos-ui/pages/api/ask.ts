import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();

  const { query, mode } = req.body;
  const backendURL = process.env.BACKEND_URL || 'http://localhost:8000';

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);

  try {
    const backendRes = await fetch(`${backendURL}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, mode }),
      signal: controller.signal,
    });

    console.log('📦 Backend response:', backendRes);
    clearTimeout(timeout);

    const data = await backendRes.json();
    console.log('📦 Data from backend:', data);
    res.status(200).json({ answer: data.answer });
  } catch {
    clearTimeout(timeout);
    res.status(500).json({ answer: 'Kairos failed to reflect. (Timeout or error)' });
  }
}
