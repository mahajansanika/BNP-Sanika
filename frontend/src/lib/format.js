export function formatMoney(amount, currency) {
  const abs = Math.abs(Number(amount)).toLocaleString('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })
  return `${amount < 0 ? '−' : ''}${currency} ${abs}`
}

export function formatMillions(amount) {
  return `${Number(amount) / 1_000_000}M`
}