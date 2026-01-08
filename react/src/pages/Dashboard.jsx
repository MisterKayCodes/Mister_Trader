import { useState, useEffect } from 'react'
import StatCard from '../components/StatCard'
import { api } from '../utils/api'

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [sessions, setSessions] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        const [statsData, sessionsData] = await Promise.all([
          api.getStats(),
          api.getSessions()
        ])
        setStats(statsData)
        setSessions(sessionsData)
      } catch (err) {
        console.error('Failed to load dashboard data:', err)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-500">Loading dashboard...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Dashboard</h2>
          <p className="text-slate-500">Your trading performance at a glance</p>
        </div>
        <button 
          onClick={() => api.exportTrades()}
          className="btn btn-secondary"
        >
          Export CSV
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard 
          label="Total Trades" 
          value={stats?.total_trades || 0}
          color="slate"
        />
        <StatCard 
          label="Win Rate" 
          value={`${stats?.win_rate || 0}%`}
          color={stats?.win_rate >= 50 ? 'green' : 'red'}
        />
        <StatCard 
          label="Total P&L" 
          value={`$${(stats?.total_pnl || 0).toLocaleString()}`}
          color={stats?.total_pnl >= 0 ? 'green' : 'red'}
        />
        <StatCard 
          label="Current Streak" 
          value={`${stats?.current_streak || 0} ${stats?.current_streak_type || ''}`}
          color={stats?.current_streak_type === 'WIN' ? 'green' : 'amber'}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Trade Breakdown</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-600">Winning Trades</span>
              <span className="font-medium text-emerald-600">{stats?.winning_trades || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-600">Losing Trades</span>
              <span className="font-medium text-red-600">{stats?.losing_trades || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-600">Breakeven</span>
              <span className="font-medium text-slate-600">{stats?.breakeven_trades || 0}</span>
            </div>
            <hr className="my-2" />
            <div className="flex justify-between">
              <span className="text-slate-600">Best Win Streak</span>
              <span className="font-medium">{stats?.best_win_streak || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-600">Worst Loss Streak</span>
              <span className="font-medium">{stats?.worst_loss_streak || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-600">Avg R:R</span>
              <span className="font-medium">{stats?.avg_risk_reward || 'N/A'}</span>
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Session Performance</h3>
          {sessions?.sessions && Object.keys(sessions.sessions).length > 0 ? (
            <div className="space-y-3">
              {Object.entries(sessions.sessions).map(([session, winRate]) => (
                <div key={session} className="flex items-center gap-4">
                  <span className="text-slate-600 w-24">{session}</span>
                  <div className="flex-1 bg-slate-100 rounded-full h-4">
                    <div 
                      className={`h-4 rounded-full ${winRate >= 50 ? 'bg-emerald-500' : 'bg-red-400'}`}
                      style={{ width: `${winRate}%` }}
                    />
                  </div>
                  <span className={`font-medium ${winRate >= 50 ? 'text-emerald-600' : 'text-red-600'}`}>
                    {winRate}%
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-slate-500">No session data yet. Close some trades to see performance.</p>
          )}
        </div>
      </div>

      <div className="card">
        <h3 className="text-lg font-semibold mb-4">Quick Stats</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-slate-50 rounded-lg">
            <p className="text-2xl font-bold text-emerald-600">${stats?.best_trade_pnl || 0}</p>
            <p className="text-sm text-slate-500">Best Trade</p>
          </div>
          <div className="text-center p-4 bg-slate-50 rounded-lg">
            <p className="text-2xl font-bold text-red-600">${stats?.worst_trade_pnl || 0}</p>
            <p className="text-sm text-slate-500">Worst Trade</p>
          </div>
          <div className="text-center p-4 bg-slate-50 rounded-lg">
            <p className="text-2xl font-bold text-indigo-600">{stats?.best_win_streak || 0}</p>
            <p className="text-sm text-slate-500">Best Streak</p>
          </div>
          <div className="text-center p-4 bg-slate-50 rounded-lg">
            <p className="text-2xl font-bold text-amber-600">{stats?.avg_risk_reward || 0}</p>
            <p className="text-sm text-slate-500">Avg R:R</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
