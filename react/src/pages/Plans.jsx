import { useState, useEffect } from 'react'
import { api } from '../utils/api'

function Plans() {
  const [plans, setPlans] = useState([])
  const [todayPlan, setTodayPlan] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    market_bias: '',
    watchlist: '',
    key_levels: '',
    mental_state: '',
    max_trades: '',
    notes: ''
  })

  useEffect(() => {
    loadPlans()
  }, [])

  async function loadPlans() {
    try {
      const [plansData, todayData] = await Promise.all([
        api.getPlans(),
        api.getTodayPlan().catch(() => null)
      ])
      setPlans(plansData)
      setTodayPlan(todayData)
    } catch (err) {
      console.error('Failed to load plans:', err)
    } finally {
      setLoading(false)
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    try {
      const submitData = {
        ...formData,
        max_trades: formData.max_trades ? parseInt(formData.max_trades) : null
      }
      await api.createPlan(submitData)
      setFormData({ title: '', market_bias: '', watchlist: '', key_levels: '', mental_state: '', max_trades: '', notes: '' })
      setShowForm(false)
      loadPlans()
    } catch (err) {
      console.error('Failed to create plan:', err)
    }
  }

  async function handleDelete(id) {
    if (!confirm('Delete this plan?')) return
    try {
      await api.deletePlan(id)
      loadPlans()
    } catch (err) {
      console.error('Failed to delete plan:', err)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-500">Loading plans...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Trading Plans</h2>
          <p className="text-slate-500">Plan your trading sessions</p>
        </div>
        <button 
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary"
        >
          {showForm ? 'Cancel' : '+ New Plan'}
        </button>
      </div>

      {todayPlan && (
        <div className="card mb-6 border-indigo-200 bg-indigo-50">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">📋</span>
            <h3 className="text-lg font-semibold text-indigo-900">Today's Plan</h3>
          </div>
          <h4 className="font-medium text-indigo-800">{todayPlan.title}</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-sm">
            {todayPlan.market_bias && (
              <div>
                <span className="text-indigo-600 font-medium">Bias: </span>
                <span className="text-indigo-800">{todayPlan.market_bias}</span>
              </div>
            )}
            {todayPlan.watchlist && (
              <div>
                <span className="text-indigo-600 font-medium">Watchlist: </span>
                <span className="text-indigo-800">{todayPlan.watchlist}</span>
              </div>
            )}
            {todayPlan.mental_state && (
              <div>
                <span className="text-indigo-600 font-medium">Mental State: </span>
                <span className="text-indigo-800">{todayPlan.mental_state}</span>
              </div>
            )}
            {todayPlan.max_trades && (
              <div>
                <span className="text-indigo-600 font-medium">Max Trades: </span>
                <span className="text-indigo-800">{todayPlan.max_trades}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {showForm && (
        <div className="card mb-6">
          <h3 className="text-lg font-semibold mb-4">Create Trading Plan</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Plan Title</label>
              <input
                type="text"
                className="input"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                required
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Market Bias</label>
                <select
                  className="input"
                  value={formData.market_bias}
                  onChange={(e) => setFormData({...formData, market_bias: e.target.value})}
                >
                  <option value="">Select...</option>
                  <option value="BULLISH">Bullish</option>
                  <option value="BEARISH">Bearish</option>
                  <option value="NEUTRAL">Neutral</option>
                </select>
              </div>
              <div>
                <label className="label">Mental State</label>
                <select
                  className="input"
                  value={formData.mental_state}
                  onChange={(e) => setFormData({...formData, mental_state: e.target.value})}
                >
                  <option value="">Select...</option>
                  <option value="Focused">Focused</option>
                  <option value="Calm">Calm</option>
                  <option value="Anxious">Anxious</option>
                  <option value="Tired">Tired</option>
                </select>
              </div>
            </div>
            <div>
              <label className="label">Watchlist (comma separated)</label>
              <input
                type="text"
                className="input"
                placeholder="EURUSD, GBPUSD, GOLD"
                value={formData.watchlist}
                onChange={(e) => setFormData({...formData, watchlist: e.target.value})}
              />
            </div>
            <div>
              <label className="label">Key Levels</label>
              <textarea
                className="input"
                rows="2"
                value={formData.key_levels}
                onChange={(e) => setFormData({...formData, key_levels: e.target.value})}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Max Trades Today</label>
                <input
                  type="number"
                  className="input"
                  value={formData.max_trades}
                  onChange={(e) => setFormData({...formData, max_trades: e.target.value})}
                />
              </div>
            </div>
            <div>
              <label className="label">Notes</label>
              <textarea
                className="input"
                rows="2"
                value={formData.notes}
                onChange={(e) => setFormData({...formData, notes: e.target.value})}
              />
            </div>
            <button type="submit" className="btn btn-success">Create Plan</button>
          </form>
        </div>
      )}

      <h3 className="text-lg font-semibold mb-4">Recent Plans</h3>
      <div className="space-y-4">
        {plans.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-slate-500">No plans yet. Create your first trading plan.</p>
          </div>
        ) : (
          plans.map((plan) => (
            <div key={plan.id} className="card">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-semibold">{plan.title}</h4>
                  <p className="text-sm text-slate-500">{plan.plan_date}</p>
                </div>
                <button 
                  onClick={() => handleDelete(plan.id)}
                  className="text-sm text-red-500 hover:text-red-700"
                >
                  Delete
                </button>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4 text-sm">
                {plan.market_bias && (
                  <div><span className="font-medium">Bias:</span> {plan.market_bias}</div>
                )}
                {plan.watchlist && (
                  <div><span className="font-medium">Watchlist:</span> {plan.watchlist}</div>
                )}
                {plan.mental_state && (
                  <div><span className="font-medium">Mental:</span> {plan.mental_state}</div>
                )}
                {plan.max_trades && (
                  <div><span className="font-medium">Max Trades:</span> {plan.max_trades}</div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Plans
