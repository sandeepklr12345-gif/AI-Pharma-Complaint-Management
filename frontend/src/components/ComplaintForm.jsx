import { useSelector, useDispatch } from 'react-redux'
import { updateField, resetForm } from '../store/complaintFormSlice'
import { saveComplaint } from '../store/complaintsListSlice'
import { useState } from 'react'

const CATEGORY_OPTIONS = [
  'Product quality',
  'Packaging defect',
  'Adverse event',
  'Labeling issue',
  'Delivery / shipping',
  'Other',
]

export default function ComplaintForm() {
  const dispatch = useDispatch()
  const { fields, aiFilledKeys } = useSelector((state) => state.complaintForm)
  const [saveState, setSaveState] = useState('idle') // idle | saving | saved | error

  const isAiFilled = (key) => aiFilledKeys.includes(key)

  const handleChange = (key) => (e) => {
    dispatch(updateField({ key, value: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSaveState('saving')
    try {
      await dispatch(saveComplaint(fields)).unwrap()
      setSaveState('saved')
      dispatch(resetForm())
    } catch {
      setSaveState('error')
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2>Log customer complaint</h2>
        <span className="hint">Fields highlighted in blue were filled by the AI copilot</span>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className={`field ${isAiFilled('complaint_id') ? 'ai-filled' : ''}`}>
            <label htmlFor="complaint_id">Complaint ID</label>
            <input
              id="complaint_id"
              value={fields.complaint_id}
              onChange={handleChange('complaint_id')}
              placeholder="CMP-2026-0001"
              required
            />
          </div>

          <div className={`field ${isAiFilled('customer_name') ? 'ai-filled' : ''}`}>
            <label htmlFor="customer_name">Customer name</label>
            <input
              id="customer_name"
              value={fields.customer_name}
              onChange={handleChange('customer_name')}
            />
          </div>

          <div className={`field ${isAiFilled('product_name') ? 'ai-filled' : ''}`}>
            <label htmlFor="product_name">Product name</label>
            <input
              id="product_name"
              value={fields.product_name}
              onChange={handleChange('product_name')}
            />
          </div>

          <div className={`field ${isAiFilled('batch_number') ? 'ai-filled' : ''}`}>
            <label htmlFor="batch_number">Batch number</label>
            <input
              id="batch_number"
              value={fields.batch_number}
              onChange={handleChange('batch_number')}
            />
          </div>

          <div className={`field ${isAiFilled('category') ? 'ai-filled' : ''}`}>
            <label htmlFor="category">Complaint category</label>
            <select id="category" value={fields.category} onChange={handleChange('category')}>
              <option value="">Select category</option>
              {CATEGORY_OPTIONS.map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>

          <div className={`field ${isAiFilled('country') ? 'ai-filled' : ''}`}>
            <label htmlFor="country">Country</label>
            <input
              id="country"
              value={fields.country}
              onChange={handleChange('country')}
            />
          </div>

          <div className="field">
            <label htmlFor="severity">Severity</label>
            <select id="severity" value={fields.severity} onChange={handleChange('severity')}>
              <option value="">Select severity</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Critical">Critical</option>
            </select>
          </div>

          <div className="field">
            <label htmlFor="status">Status</label>
            <select id="status" value={fields.status} onChange={handleChange('status')}>
              <option value="New">New</option>
              <option value="Under Review">Under review</option>
              <option value="Closed">Closed</option>
            </select>
          </div>

          <div className={`field span-2 ${isAiFilled('description') ? 'ai-filled' : ''}`}>
            <label htmlFor="description">Complaint description</label>
            <textarea
              id="description"
              value={fields.description}
              onChange={handleChange('description')}
              placeholder="What happened, when, and to which product?"
            />
          </div>
        </div>

        <div className="copilot-actions">
          <button type="submit" className="btn btn-primary" disabled={saveState === 'saving'}>
            {saveState === 'saving' ? 'Saving…' : 'Save complaint'}
          </button>
          <button type="button" className="btn btn-secondary" onClick={() => dispatch(resetForm())}>
            Clear form
          </button>
        </div>
        {saveState === 'saved' && <p className="status-line">Complaint saved.</p>}
        {saveState === 'error' && <p className="status-line error">Couldn't save — check the backend is running.</p>}
      </form>
    </div>
  )
}
