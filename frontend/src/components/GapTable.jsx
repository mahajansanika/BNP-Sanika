import { formatMoney } from '../lib/format'

const th = 'px-3 py-2 font-medium'

export function GapTable({ data }) {
  return (
    <div className="mt-4 overflow-x-auto rounded-lg border border-slate-200 bg-white">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-slate-500">
          <tr>
            <th className={`${th} text-left`}>Bucket</th>
            <th className={`${th} text-right`}>Assets</th>
            <th className={`${th} text-right`}>Liabilities</th>
            <th className={`${th} text-right`}>Net gap</th>
            <th className={`${th} text-left`}>Position</th>
          </tr>
        </thead>
        <tbody>
          {data.buckets.map((b) => {
            const short = b.net_gap < 0
            return (
              <tr key={b.bucket} className="border-t border-slate-100">
                <td className="px-3 py-2 font-medium">{b.bucket}</td>
                <td className="px-3 py-2 text-right tabular-nums">
                  {formatMoney(b.assets, data.currency)}
                </td>
                <td className="px-3 py-2 text-right tabular-nums">
                  {formatMoney(b.liabilities, data.currency)}
                </td>
                <td
                  className={`px-3 py-2 text-right font-medium tabular-nums ${
                    short ? 'text-red-700' : 'text-slate-900'
                  }`}
                >
                  {formatMoney(b.net_gap, data.currency)}
                </td>
                <td className="px-3 py-2">{short ? 'Shortfall' : 'Surplus'}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}