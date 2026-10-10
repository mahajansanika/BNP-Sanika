import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { formatMillions, formatMoney } from '../lib/format'

export function LadderChart({ data }) {
  return (
    <div className="h-80 rounded-lg border border-slate-200 bg-white p-3">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data.buckets}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="bucket" />
          <YAxis tickFormatter={formatMillions} />
          <Tooltip formatter={(value) => formatMoney(value, data.currency)} />
          <Legend />
          <Bar dataKey="assets" name="Assets" fill="#0d9488" />
          <Bar dataKey="liabilities" name="Liabilities" fill="#475569" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}