import { useState } from 'react'

function Settings() {
  const [token, setToken] = useState(localStorage.getItem('token') || '')

  function handleSaveToken() {
    localStorage.setItem('token', token)
    alert('Token saved!')
  }

  function handleClearToken() {
    localStorage.removeItem('token')
    setToken('')
    alert('Token cleared!')
  }

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-slate-900">Settings</h2>
        <p className="text-slate-500">Configure your trading journal</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Authentication</h3>
          <p className="text-sm text-slate-600 mb-4">
            Enter your API token to access your trading data. Get your token from the Telegram bot.
          </p>
          <div className="space-y-4">
            <div>
              <label className="label">API Token</label>
              <input
                type="password"
                className="input"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="Enter your API token"
              />
            </div>
            <div className="flex gap-2">
              <button onClick={handleSaveToken} className="btn btn-primary">
                Save Token
              </button>
              <button onClick={handleClearToken} className="btn btn-secondary">
                Clear Token
              </button>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">About</h3>
          <div className="space-y-3 text-sm text-slate-600">
            <p><strong>Mister Trader</strong> - Your personal trading journal</p>
            <p>Track your trades, analyze performance, and improve your trading through data-driven insights.</p>
            <div className="pt-4 border-t border-slate-100">
              <p><strong>Features:</strong></p>
              <ul className="list-disc list-inside mt-2 space-y-1">
                <li>Trade logging via Telegram bot</li>
                <li>Session performance analysis</li>
                <li>Strategy tracking</li>
                <li>Daily trading plans</li>
                <li>CSV export</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
          <div className="space-y-3">
            <a 
              href="/api/docs" 
              target="_blank" 
              className="block p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors"
            >
              <span className="font-medium">API Documentation</span>
              <p className="text-sm text-slate-500">View the API docs</p>
            </a>
            <a 
              href="#" 
              className="block p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors"
            >
              <span className="font-medium">Telegram Bot</span>
              <p className="text-sm text-slate-500">Open the trading bot</p>
            </a>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Data Management</h3>
          <div className="space-y-4">
            <button 
              onClick={() => window.open('/api/v1/export/trades/csv', '_blank')}
              className="btn btn-secondary w-full"
            >
              Export All Trades (CSV)
            </button>
            <p className="text-xs text-slate-500">
              Export all your trading data to a CSV file that you can open in Excel or Google Sheets.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings
