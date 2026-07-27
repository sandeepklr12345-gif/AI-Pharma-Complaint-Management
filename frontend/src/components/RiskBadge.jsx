export default function RiskBadge({ level }) {
  const safeLevel = level && ['Low', 'Medium', 'High', 'Critical'].includes(level) ? level : 'Unknown'
  return <span className={`badge badge-${safeLevel}`}>{safeLevel}</span>
}
