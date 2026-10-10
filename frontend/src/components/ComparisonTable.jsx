import { formatMoney } from '../lib/format'

function verdict(det, ai) {
  if (det >= 0 && ai < 0) return 'Hidden shortfall'
  if (det < 0 && ai >= 0) return 'Shortfall resolved'
  return '—'
}

export function ComparisonTable({ deterministic, ai }) {
  const currency = ai.currency

  return (
    <div className="mt-4 overflow-x-auto rounded-lg border border-slate-200 bg-white">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-slate-500">
          <tr>
            <th className="px-3 py-2 text-left font-medium">Bucket</th>
            <th className="px-3 py-2 text-right font-medium">Deterministic net gap</th>
            <th className="px-3 py-2 text-right font-medium">AI-adjusted net gap</th>
            <th className="px-3 py-2 text-right font-medium">Difference</th>
            <th className="px-3 py-2 text-left font-medium">What changes</th>
          </tr>
        </thead>
        <tbody>
          {ai.buckets.map((aiRow) => {
            const detRow = deterministic.buckets.find((b) => b.bucket === aiRow.bucket)
            const diff = aiRow.net_gap - detRow.net_gap
            const text = verdict(detRow.net_gap, aiRow.net_gap)
            return (
              <tr key={aiRow.bucket} className="border-t border-slate-100">
                <td className="px-3 py-2 font-medium">{aiRow.bucket}</td>
                <td className="px-3 py-2 text-right tabular-nums">
                  {formatMoney(detRow.net_gap, currency)}
                </td>
                <td className="px-3 py-2 text-right tabular-nums">
                  {formatMoney(aiRow.net_gap, currency)}
                </td>
                <td className="px-3 py-2 text-right tabular-nums">
                  {diff > 0 ? '+' : ''}
                  {formatMoney(diff, currency)}
                </td>
                <td
                  className={`px-3 py-2 ${
                    text === 'Hidden shortfall' ? 'font-medium text-red-700' : ''
                  }`}
                >
                  {text}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}