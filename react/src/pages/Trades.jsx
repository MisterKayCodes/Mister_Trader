import { useState, useEffect } from 'react'
import { api } from '../utils/api'

function Trades() {
  const [trades, setTrades] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadTrades() {
      try {
        const data = await api.getTrades()
        setTrades(data.trades || data || [])
      } catch (err) {
        console.error('Failed to load trades:', err)
      } finally {
        setLoading(false)
      }
    }
    loadTrades()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-500">Loading trades...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Trade Journal</h2>
          <p className="text-slate-500">Review and analyze your trades</p>
        </div>
        <button 
          onClick={() => api.exportTrades()}
          className="btn btn-primary"
        >
          Export to CSV
        </button>
      </div>

      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-600">Symbol</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-600">Side</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-600">Entry</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-600">Exit</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-600">P&L</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-600">Outcome</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-600">Session</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-slate-600">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {trades.length === 0 ? (
                <tr>
                  <td colSpan="8" className="px-4 py-8 text-center text-slate-500">
                    No trades yet. Start logging trades via the Telegram bot.
                  </td>
                </tr>
              ) : (
                trades.map((trade) => (
                  <tr key={trade.id} className="hover:bg-slate-50">
                    <td className="px-4 py-3 font-medium">{trade.symbol}</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        trade.side === 'BUY' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
                      }`}>
                        {trade.side}
                      </span>
                    </td>
                    <td className="px-4 py-3">{trade.entry_price || '-'}</td>
                    <td className="px-4 py-3">{trade.exit_price || '-'}</td>
                    <td className={`px-4 py-3 font-medium ${
                      trade.pnl >= 0 ? 'text-emerald-600' : 'text-red-600'
                    }`}>
                      {trade.pnl != null ? `$${trade.pnl.toFixed(2)}` : '-'}
                    </td>
                    <td className="px-4 py-3">
                      {trade.outcome && (
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          trade.outcome === 'WIN' ? 'bg-emerald-100 text-emerald-700' :
                          trade.outcome === 'LOSS' ? 'bg-red-100 text-red-700' :
                          'bg-slate-100 text-slate-700'
                        }`}>
                          {trade.outcome}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-3 text-slate-500">{trade.trading_session || '-'}</td>
                    <td className="px-4 py-3 text-slate-500">
                      {trade.created_at ? new Date(trade.created_at).toLocaleDateString() : '-'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Trades
