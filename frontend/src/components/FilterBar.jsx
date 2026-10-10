import { CURRENCIES, LOCATIONS, useFilters } from '../lib/filters'

const control =
  'rounded-md border border-slate-300 bg-white px-2 py-1.5 text-sm text-slate-800'

export function FilterBar() {
  const [filters, setFilter] = useFilters()

  return (
    <div className="mb-4 flex flex-wrap items-end gap-4 rounded-lg border border-slate-200 bg-white p-3">
      <label className="flex flex-col gap-1 text-xs text-slate-500">
        Currency
        <select
          className={control}
          value={filters.currency}
          onChange={(e) => setFilter('currency', e.target.value)}
        >
          {CURRENCIES.map((c) => (
            <option key={c}>{c}</option>
          ))}
        </select>
      </label>

      <label className="flex flex-col gap-1 text-xs text-slate-500">
        Location
        <select
          className={control}
          value={filters.location}
          onChange={(e) => setFilter('location', e.target.value)}
        >
          {LOCATIONS.map((l) => (
            <option key={l}>{l}</option>
          ))}
        </select>
      </label>

      <label className="flex flex-col gap-1 text-xs text-slate-500">
        Calculation date
        <input
          type="date"
          className={control}
          value={filters.calc_date}
          onChange={(e) => setFilter('calc_date', e.target.value)}
        />
      </label>
    </div>
  )
}