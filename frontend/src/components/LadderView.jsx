import { useState } from 'react'
import { useLadder } from '../api/hooks'
import { DrillDownTable } from './DrillDownTable'
import { FilterBar } from './FilterBar'
import { GapTable } from './GapTable'
import { LadderChart } from './LadderChart'

export function LadderView({ approach, title }) {
  const [selected, setSelected] = useState(null)
  const { data, isLoading, error } = useLadder(approach)

  return (
    <div>
      <h1 className="mb-4 text-xl font-semibold">{title}</h1>
      <FilterBar />

      {isLoading && <p className="text-sm text-slate-500">Loading ladder…</p>}
      {error && <p className="text-sm text-red-700">{error.message}</p>}

      {data && (
        <>
          {data.matured_count > 0 && (
            <p className="mb-4 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900">
              {data.matured_count} {data.matured_count === 1 ? 'position' : 'positions'} matured
              before the calculation date and left out of this ladder.
            </p>
          )}
          <LadderChart data={data} />
          <GapTable data={data} onSelect={setSelected} />
          {selected && (
            <DrillDownTable
              key={selected}
              approach={approach}
              bucket={selected}
              currency={data.currency}
              onClose={() => setSelected(null)}
            />
          )}
        </>
      )}
    </div>
  )
}