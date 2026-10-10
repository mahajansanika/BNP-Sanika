import { FilterBar } from '../components/FilterBar'
import { useLadder } from '../api/hooks'

export function DeterministicPage() {
  const { data, isLoading, error } = useLadder('deterministic')

  return (
    <div>
      <h1 className="mb-4 text-xl font-semibold">Deterministic ladder</h1>
      <FilterBar />

      {isLoading && <p className="text-sm text-slate-500">Loading ladder…</p>}
      {error && <p className="text-sm text-red-600">{error.message}</p>}
      {data && (
        <pre className="text-xs text-slate-600">
          {JSON.stringify(data.buckets, null, 2)}
        </pre>
      )}
    </div>
  )
}