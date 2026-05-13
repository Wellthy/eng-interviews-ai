import { useState } from 'react';
import { classifyMessage, type ClassifyResponse } from '../api/classify';
import { ClassificationResult } from './ClassificationResult';

type Status = 'idle' | 'loading' | 'error';

export function MessageClassifier() {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState<ClassifyResponse | null>(null);
  const [status, setStatus] = useState<Status>('idle');

  const trimmed = message.trim();
  const canSubmit = trimmed.length > 0 && status !== 'loading';

  async function handleSubmit() {
    if (!canSubmit) return;
    setStatus('loading');
    setResult(null);
    try {
      const data = await classifyMessage(trimmed);
      setResult(data);
      setStatus('idle');
    } catch (err) {
      console.error(err);
      setStatus('error');
    }
  }

  return (
    <div className="mb-5 border border-gray-300 p-5">
      <h2 className="mb-2 text-xl font-semibold">Send a Message</h2>
      <textarea
        className="mb-2 h-24 w-full rounded border border-gray-300 p-2"
        placeholder="Type your message here..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button
        type="button"
        onClick={handleSubmit}
        disabled={!canSubmit}
        className="cursor-pointer rounded bg-blue-600 px-5 py-2 text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {status === 'loading' ? 'Checking...' : 'Check Urgency'}
      </button>

      {status === 'loading' && (
        <div className="mt-5 rounded p-4">Processing...</div>
      )}
      {status === 'error' && (
        <div className="mt-5 rounded bg-red-100 p-4 text-red-900">
          Error: Could not classify message. Please try again.
        </div>
      )}
      {status === 'idle' && result && <ClassificationResult result={result} />}
    </div>
  );
}
