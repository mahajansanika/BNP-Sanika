import { useQuery } from '@tanstack/react-query'
import { useFilters } from '../lib/filters'
import { getLadder } from './client'

export function useLadder(approach) {
  const [filters] = useFilters()

  return useQuery({
    queryKey: ['ladder', approach, filters],
    queryFn: () => getLadder(approach, filters),
  })
}