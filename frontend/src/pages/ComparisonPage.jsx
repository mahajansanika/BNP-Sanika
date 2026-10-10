import { useLadder } from '../api/hooks'
import { ComparisonTable } from '../components/ComparisonTable'
import { FilterBar } from '../components/FilterBar'

export function ComparisonPage() {
  const deterministic = useLadder('deterministic')
  const ai = useLadder('ai')

  const isLoading = deterministic.isLoading || ai.isLoading
  const error = deterministic.error || ai.error

  return (
    <div>
      <h1 className="mb-4 text-xl font-semibold">Comparison</h1>
      <FilterBar />

      {isLoading && <p className="text-sm text-slate-500">Loading both ladders…</p>}
      {error && <p className="text-sm text-red-700">{error.message}</p>}

      {deterministic.data && ai.data && (
        <ComparisonTable deterministic={deterministic.data} ai={ai.data} />
      )}

      <section className="mt-6 rounded-lg border border-dashed border-slate-300 p-4 text-sm text-slate-500">
        Recommendations will appear here (Dev 5's panel).
      </section>
    </div>
  )
}