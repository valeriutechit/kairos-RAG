import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).end();
  const { query, mode } = req.body;

  try {
    const backendURL = process.env.BACKEND_URL || 'http://localhost:8000';

    const backendRes = await fetch(`${backendURL}/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, mode }),
    });
    const data = await backendRes.json();
    res.status(200).json({ answer: data.answer });
  } catch {
    res.status(500).json({ answer: 'Kairos failed to reflect.' });
  }
}
