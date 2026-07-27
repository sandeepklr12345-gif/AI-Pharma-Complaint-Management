import { useState } from 'react'
import ComplaintForm from './components/ComplaintForm'
import AiCopilotPanel from './components/AiCopilotPanel'
import ComplaintsList from './components/ComplaintsList'

export default function App() {
  const [tab, setTab] = useState('new') // 'new' | 'list'

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>Customer complaint management</h1>
          <div className="subtitle">AI-powered intake for pharmaceutical quality complaints</div>
        </div>
        <div className="tabs">
          <button
            className={`tab-btn ${tab === 'new' ? 'active' : ''}`}
            onClick={() => setTab('new')}
          >
            New complaint
          </button>
          <button
            className={`tab-btn ${tab === 'list' ? 'active' : ''}`}
            onClick={() => setTab('list')}
          >
            All complaints
          </button>
        </div>
      </header>

      <main className="app-body">
        {tab === 'new' ? (
          <div className="workspace-grid">
            <ComplaintForm />
            <AiCopilotPanel />
          </div>
        ) : (
          <ComplaintsList />
        )}
      </main>
    </div>
  )
}
