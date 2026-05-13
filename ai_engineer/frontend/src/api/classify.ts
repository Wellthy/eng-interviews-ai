export type ClassifyResponse = {
  urgent: boolean;
  confidence_score: number;
  reasoning: string;
  model_version: string;
};

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

export async function classifyMessage(text: string): Promise<ClassifyResponse> {
  const response = await fetch(`${API_URL}/classify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return (await response.json()) as ClassifyResponse;
}
