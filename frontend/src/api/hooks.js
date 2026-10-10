import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useFilters } from '../lib/filters'
import { getLadder, getPositions } from './client'

export function useLadder(approach) {
  const [filters] = useFilters()

  return useQuery({
    queryKey: ['ladder', approach, filters],
    queryFn: () => getLadder(approach, filters),
  })
}

export const PAGE_SIZE = 5

export function usePositions(approach, bucket, page) {
  const [filters] = useFilters()

  return useQuery({
    queryKey: ['positions', approach, bucket, page, filters],
    queryFn: () => getPositions(approach, bucket, filters, page, PAGE_SIZE),
    placeholderData: keepPreviousData,
  })
}