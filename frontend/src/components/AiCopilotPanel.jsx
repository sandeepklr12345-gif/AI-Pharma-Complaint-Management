import { useRef } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { setInputText, uploadFile, analyzeText, clearResult } from '../store/aiCopilotSlice'
import { fillFromAi } from '../store/complaintFormSlice'
import RiskBadge from './RiskBadge'

export default function AiCopilotPanel() {
  const dispatch = useDispatch()
  const { inputText, status, result, error } = useSelector((state) => state.aiCopilot)
  const fileInputRef = useRef(null)

  const isBusy = status === 'uploading' || status === 'analyzing'

  const handleFileChange = (e) => {
    const file = e.target.files?.[0]
    if (file) dispatch(uploadFile(file))
    e.target.value = '' // allow re-uploading the same file
  }

  const handleAnalyze = () => {
    if (inputText.trim()) dispatch(analyzeText(inputText))
  }

  const handleFillForm = () => {
    if (result) dispatch(fillFromAi(result.extracted_fields))
  }

  return (
    <div className="card copilot-card" data-risk={result?.risk_level}>
      <div className="card-header">
        <h2>AI copilot</h2>
        <span className="hint">Paste a complaint, or upload a PDF/email</span>
      </div>

      <div className="field">
        <label htmlFor="ai-input">Complaint text</label>
        <textarea
          id="ai-input"
          rows={6}
          value={inputText}
          onChange={(e) => dispatch(setInputText(e.target.value))}
          placeholder="Paste the complaint email or extracted text here…"
        />
      </div>

      <input
        type="file"
        accept=".pdf,.txt,.eml"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />

      <div className="copilot-actions">
        <button
          type="button"
          className="btn btn-secondary"
          onClick={() => fileInputRef.current?.click()}
          disabled={isBusy}
        >
          {status === 'uploading' ? 'Uploading…' : 'Upload file'}
        </button>
        <button
          type="button"
          className="btn btn-primary"
          onClick={handleAnalyze}
          disabled={isBusy || !inputText.trim()}
        >
          {status === 'analyzing' ? 'Analyzing…' : 'Analyze complaint'}
        </button>
      </div>

      {status === 'error' && <p className="status-line error">{error}</p>}

      {result && (
        <div className="copilot-result">
          <div className="result-row">
            <div className="label">Risk assessment</div>
            <p><RiskBadge level={result.risk_level} /> &nbsp; {result.risk_reason}</p>
          </div>

          <div className="result-row">
            <div className="label">Summary</div>
            <p>{result.summary}</p>
          </div>

          {result.missing_fields?.length > 0 && (
            <div className="result-row">
              <div className="missing-fields-warning">
                Missing: {result.missing_fields.join(', ')}
              </div>
            </div>
          )}

          {result.duplicate_match && (
            <div className="result-row">
              <div className="duplicate-warning">
                Possible duplicate of complaint #{result.duplicate_match.complaint_id}
                {' '}({Math.round(result.duplicate_match.similarity_score * 100)}% similar)
              </div>
            </div>
          )}

          <div className="copilot-actions">
            <button type="button" className="btn btn-primary btn-block" onClick={handleFillForm}>
              Fill form with AI results
            </button>
          </div>

          <button
            type="button"
            className="btn btn-secondary btn-block"
            style={{ marginTop: 8 }}
            onClick={() => dispatch(clearResult())}
          >
            Clear results
          </button>
        </div>
      )}
    </div>
  )
}
