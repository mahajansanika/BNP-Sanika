import { useSearchParams } from 'react-router-dom'

export const CURRENCIES = ['USD', 'EUR', 'GBP', 'SGD', 'HKD']
export const LOCATIONS = ['Hong Kong', 'New York', 'London', 'Singapore', 'Paris']

const today = () => new Date().toISOString().slice(0, 10)

export function useFilters() {
  const [params, setParams] = useSearchParams()

  const filters = {
    currency: params.get('currency') ?? 'EUR',
    location: params.get('location') ?? 'London',
    calc_date: params.get('calc_date') ?? today(),
  }

  function setFilter(name, value) {
    const next = new URLSearchParams(params)
    next.set(name, value)
    setParams(next, { replace: true })
  }

  return [filters, setFilter]
}