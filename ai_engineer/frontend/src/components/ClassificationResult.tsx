import type { ClassifyResponse } from '../api/classify';

type Props = { result: ClassifyResponse };

export function ClassificationResult({ result }: Props) {
  const palette = result.urgent
    ? 'bg-red-100 text-red-900'
    : 'bg-green-100 text-green-900';
  const headline = result.urgent
    ? '🚨 This message appears to be URGENT!'
    : '✅ This message does not appear urgent.';
  const pct = Math.max(0, Math.min(1, result.confidence_score)) * 100;

  return (
    <div className={`mt-5 rounded p-4 ${palette}`}>
      <div>{headline}</div>
      <div className="mt-2 border-t border-black/10 pt-2 text-sm">
        <div>
          <strong>Confidence:</strong> {pct.toFixed(1)}%
        </div>
        <div className="mt-1 h-2 w-full overflow-hidden rounded bg-black/10">
          <div className="h-full bg-current" style={{ width: `${pct}%` }} />
        </div>
        <div className="mt-2">
          <strong>Reasoning:</strong> {result.reasoning}
        </div>
        <div className="mt-1 text-xs opacity-80">
          Model: v{result.model_version}
        </div>
      </div>
    </div>
  );
}
