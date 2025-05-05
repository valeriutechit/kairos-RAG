'use client';

import { useState } from 'react';

const MODES = ['default', 'stoic', 'trickster', 'dark'];

export default function Home() {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState('default');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, mode }),
      });
      const data = await res.json();
      setResponse(data.answer);
    } catch {
      setResponse('Kairos is silent.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-4 py-10">
      <h1 className="text-4xl font-bold mb-6">Kairos</h1>
      <p className="text-gray-400 text-sm mb-8">Kairos doesn’t answer. It reflects.</p>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
        className="w-full max-w-xl p-3 bg-zinc-900 border border-zinc-700 text-white rounded-md"
        placeholder="Ask Kairos..."
      />

      <div className="mt-4">
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          className="bg-zinc-900 border border-zinc-700 text-white rounded px-4 py-2"
        >
          {MODES.map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>
      </div>

      <button
        onClick={handleAsk}
        disabled={loading}
        className="mt-4 px-6 py-2 bg-white text-black font-semibold rounded hover:bg-gray-200"
      >
        {loading ? 'Reflecting...' : 'Ask'}
      </button>

      {response && (
        <div className="mt-10 max-w-2xl bg-zinc-900 p-6 border border-zinc-700 rounded text-white">
          {response}
        </div>
      )}
    </main>
  );
}
