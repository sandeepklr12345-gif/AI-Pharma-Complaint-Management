import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { fetchComplaints } from '../store/complaintsListSlice'
import RiskBadge from './RiskBadge'

export default function ComplaintsList() {
  const dispatch = useDispatch()
  const { items, status } = useSelector((state) => state.complaintsList)

  useEffect(() => {
    dispatch(fetchComplaints())
  }, [dispatch])

  return (
    <div className="card">
      <div className="card-header">
        <h2>All complaints</h2>
        <span className="hint">{items.length} logged</span>
      </div>

      {status === 'loading' && <p className="status-line">Loading…</p>}

      {status !== 'loading' && items.length === 0 && (
        <div className="empty-state">No complaints logged yet.</div>
      )}

      {items.length > 0 && (
        <table className="complaints-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Product</th>
              <th>Batch</th>
              <th>Category</th>
              <th>Risk</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {items.map((c) => (
              <tr key={c.id}>
                <td>{c.complaint_id}</td>
                <td>{c.product_name || '—'}</td>
                <td>{c.batch_number || '—'}</td>
                <td>{c.category || '—'}</td>
                <td><RiskBadge level={c.ai_risk_level} /></td>
                <td>{c.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
