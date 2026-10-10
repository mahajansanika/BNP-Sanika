// Hand-written answers shaped like the real API. Used while VITE_USE_MOCKS is on.

const BUCKETS = ['0-1M', '1-3M', '3-12M', '1-5Y', '>5Y']

// One bucket row. net_gap is worked out here so the numbers can never disagree.
function row(bucket, assets, liabilities, count) {
  return {
    bucket,
    assets,
    liabilities,
    net_gap: assets - liabilities,
    transaction_count: count,
  }
}

const DETERMINISTIC = [
  row('0-1M', 10_000_000, 6_000_000, 7),
  row('1-3M', 4_000_000, 8_200_000, 5),
  row('3-12M', 9_000_000, 7_000_000, 9),
  row('1-5Y', 6_000_000, 8_000_000, 8),
  row('>5Y', 5_000_000, 3_000_000, 6),
]

// Two 3.5M deposits move from 1-3M into 0-1M, so 0-1M flips to a shortfall.
const AI = [
  row('0-1M', 10_000_000, 13_000_000, 9),
  row('1-3M', 4_000_000, 1_200_000, 3),
  row('3-12M', 9_000_000, 7_000_000, 9),
  row('1-5Y', 6_000_000, 8_000_000, 8),
  row('>5Y', 5_000_000, 3_000_000, 6),
]

// query = { calc_date, currency, location, run_id }
export function getMockLadder(approach, query) {
  return {
    run_id: query.run_id,
    calc_date: query.calc_date,
    currency: query.currency,
    location: query.location,
    approach,
    buckets: approach === 'ai' ? AI : DETERMINISTIC,
    matured_count: 1,
  }
}

export { BUCKETS }

const POSITIONS_0_1M = [
  { id: 'P-1001', type: 'asset', product: 'Reverse repo', amount: 4000000, maturity_date: '2026-10-14' },
  { id: 'P-1002', type: 'asset', product: 'Treasury bill', amount: 3000000, maturity_date: '2026-10-17' },
  { id: 'P-1003', type: 'asset', product: 'Interbank loan', amount: 2000000, maturity_date: '2026-10-22' },
  { id: 'P-1004', type: 'asset', product: 'Corporate bond', amount: 1000000, maturity_date: '2026-11-02' },
  { id: 'P-2001', type: 'liability', product: 'Customer deposit', amount: 3000000, maturity_date: '2026-10-28' },
  { id: 'P-2002', type: 'liability', product: 'Interbank borrowing', amount: 2000000, maturity_date: '2026-11-05' },
  { id: 'P-2003', type: 'liability', product: 'Repo', amount: 1000000, maturity_date: '2026-11-08' },
]

export function getMockPositions(bucket, { page, page_size }) {
  const all = bucket === '0-1M' ? POSITIONS_0_1M : []
  const start = (page - 1) * page_size
  return { bucket, page, page_size, total: all.length, items: all.slice(start, start + page_size) }
}