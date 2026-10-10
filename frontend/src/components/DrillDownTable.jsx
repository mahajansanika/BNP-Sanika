import { useState } from 'react'
import { PAGE_SIZE, usePositions } from '../api/hooks'
import { formatMoney } from '../lib/format'

const pagerButton =
  'rounded-md border border-slate-300 px-3 py-1 text-sm hover:bg-slate-50 disabled:opacity-40'

export function DrillDownTable({ approach, bucket, currency, onClose }) {
  const [page, setPage] = useState(1)
  const { data, isLoading, error } = usePositions(approach, bucket, page)
  const pages = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1

  return (
    <section className="mt-6 rounded-lg border border-slate-200 bg-white">
      <div className="flex items-center justify-between border-b border-slate-100 px-3 py-2">
        <h2 className="font-semibold">Positions in {bucket}</h2>
        <button onClick={onClose} className="rounded-md px-2 py-1 text-sm hover:bg-slate-100">
          Close
        </button>
      </div>

      {isLoading && <p className="p-3 text-sm text-slate-500">Loading positions…</p>}
      {error && <p className="p-3 text-sm text-red-700">{error.message}</p>}
      {data && data.total === 0 && (
        <p className="p-3 text-sm text-slate-500">No positions in this bucket.</p>
      )}

      {data && data.total > 0 && (
        <>
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-slate-500">
              <tr>
                <th className="px-3 py-2 text-left font-medium">Product</th>
                <th className="px-3 py-2 text-left font-medium">Type</th>
                <th className="px-3 py-2 text-left font-medium">Maturity</th>
                <th className="px-3 py-2 text-right font-medium">Amount</th>
              </tr>
            </thead>
            <tbody>
              {data.items.map((p) => (
                <tr key={p.id} className="border-t border-slate-100">
                  <td className="px-3 py-2">{p.product}</td>
                  <td className="px-3 py-2 capitalize">{p.type}</td>
                  <td className="px-3 py-2 tabular-nums">{p.maturity_date}</td>
                  <td className="px-3 py-2 text-right tabular-nums">
                    {formatMoney(p.amount, currency)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="flex items-center justify-end gap-3 border-t border-slate-100 px-3 py-2 text-sm">
            <span className="text-slate-500">
              Page {page} of {pages}
            </span>
            <button className={pagerButton} disabled={page <= 1} onClick={() => setPage(page - 1)}>
              Previous
            </button>
            <button className={pagerButton} disabled={page >= pages} onClick={() => setPage(page + 1)}>
              Next
            </button>
          </div>
        </>
      )}
    </section>
  )
}