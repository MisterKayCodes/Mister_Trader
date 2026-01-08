import { useState, useEffect } from 'react'
import { api } from '../utils/api'

function Strategies() {
  const [strategies, setStrategies] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    entry_criteria: '',
    exit_criteria: '',
    risk_per_trade: ''
  })

  useEffect(() => {
    loadStrategies()
  }, [])

  async function loadStrategies() {
    try {
      const data = await api.getStrategiesList()
      setStrategies(data)
    } catch (err) {
      console.error('Failed to load strategies:', err)
    } finally {
      setLoading(false)
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    try {
      await api.createStrategy(formData)
      setFormData({ name: '', description: '', entry_criteria: '', exit_criteria: '', risk_per_trade: '' })
      setShowForm(false)
      loadStrategies()
    } catch (err) {
      console.error('Failed to create strategy:', err)
    }
  }

  async function handleDelete(id) {
    if (!confirm('Delete this strategy?')) return
    try {
      await api.deleteStrategy(id)
      loadStrategies()
    } catch (err) {
      console.error('Failed to delete strategy:', err)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-slate-500">Loading strategies...</div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Strategies</h2>
          <p className="text-slate-500">Define and track your trading strategies</p>
        </div>
        <button 
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary"
        >
          {showForm ? 'Cancel' : '+ New Strategy'}
        </button>
      </div>

      {showForm && (
        <div className="card mb-6">
          <h3 className="text-lg font-semibold mb-4">Create New Strategy</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Strategy Name</label>
              <input
                type="text"
                className="input"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
              />
            </div>
            <div>
              <label className="label">Description</label>
              <textarea
                className="input"
                rows="2"
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Entry Criteria</label>
                <textarea
                  className="input"
                  rows="2"
                  value={formData.entry_criteria}
                  onChange={(e) => setFormData({...formData, entry_criteria: e.target.value})}
                />
              </div>
              <div>
                <label className="label">Exit Criteria</label>
                <textarea
                  className="input"
                  rows="2"
                  value={formData.exit_criteria}
                  onChange={(e) => setFormData({...formData, exit_criteria: e.target.value})}
                />
              </div>
            </div>
            <div>
              <label className="label">Risk Per Trade</label>
              <input
                type="text"
                className="input"
                placeholder="e.g., 1%"
                value={formData.risk_per_trade}
                onChange={(e) => setFormData({...formData, risk_per_trade: e.target.value})}
              />
            </div>
            <button type="submit" className="btn btn-success">Create Strategy</button>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {strategies.length === 0 ? (
          <div className="card col-span-full text-center py-12">
            <p className="text-slate-500">No strategies yet. Create one to start tracking performance.</p>
          </div>
        ) : (
          strategies.map((strategy) => (
            <div key={strategy.id} className="card">
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-lg font-semibold">{strategy.name}</h3>
                <span className={`px-2 py-1 rounded text-xs ${
                  strategy.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-600'
                }`}>
                  {strategy.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              {strategy.description && (
                <p className="text-slate-600 text-sm mb-3">{strategy.description}</p>
              )}
              <div className="space-y-2 text-sm">
                {strategy.entry_criteria && (
                  <div>
                    <span className="font-medium text-slate-700">Entry: </span>
                    <span className="text-slate-600">{strategy.entry_criteria}</span>
                  </div>
                )}
                {strategy.exit_criteria && (
                  <div>
                    <span className="font-medium text-slate-700">Exit: </span>
                    <span className="text-slate-600">{strategy.exit_criteria}</span>
                  </div>
                )}
                {strategy.risk_per_trade && (
                  <div>
                    <span className="font-medium text-slate-700">Risk: </span>
                    <span className="text-slate-600">{strategy.risk_per_trade}</span>
                  </div>
                )}
              </div>
              <div className="mt-4 pt-4 border-t border-slate-100">
                <button 
                  onClick={() => handleDelete(strategy.id)}
                  className="text-sm text-red-500 hover:text-red-700"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default Strategies
