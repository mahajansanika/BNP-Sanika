import { getMockLadder } from './api/mockData'

export default function App() {
  const ladder = getMockLadder('ai', {
    calc_date: '2026-10-10',
    currency: 'EUR',
    location: 'London',
    run_id: 1,
  })
  return (
    <div className="min-h-screen bg-slate-100 p-8">
      <h1 className="text-2xl font-semibold text-teal-700">Liquid+</h1>
      <pre className="mt-4 rounded bg-white p-4 text-xs">{JSON.stringify(ladder, null, 2)}</pre>
    </div>
  )
}