import { FilterBar } from '../components/FilterBar'
import { useFilters } from '../lib/filters'

export function DeterministicPage() {
  const [filters] = useFilters()

  return (
    <div>
      <h1 className="mb-4 text-xl font-semibold">Deterministic ladder</h1>
      <FilterBar />
      <pre className="text-xs text-slate-500">{JSON.stringify(filters, null, 2)}</pre>
    </div>
  )
}