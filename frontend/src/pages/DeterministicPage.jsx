import { FilterBar } from '../components/FilterBar'
import { useLadder } from '../api/hooks'
import { LadderChart } from '../components/LadderChart'
import { GapTable } from '../components/GapTable'

export function DeterministicPage() {
  const { data, isLoading, error } = useLadder('deterministic')

  return (
    <div>
      <h1 className="mb-4 text-xl font-semibold">Deterministic ladder</h1>
      <FilterBar />

      {isLoading && <p className="text-sm text-slate-500">Loading ladder…</p>}
      {error && <p className="text-sm text-red-600">{error.message}</p>}
      {data && (
  <>
    <LadderChart data={data} />
    <GapTable data={data} />
  </>
)}
    </div>
  )
}