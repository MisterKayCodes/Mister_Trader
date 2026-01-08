const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  { id: 'trades', label: 'Trade Journal', icon: '📈' },
  { id: 'strategies', label: 'Strategies', icon: '🎯' },
  { id: 'plans', label: 'Trading Plans', icon: '📋' },
  { id: 'settings', label: 'Settings', icon: '⚙️' },
]

function Sidebar({ currentPage, setCurrentPage }) {
  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-slate-900 text-white p-6">
      <div className="mb-8">
        <h1 className="text-xl font-bold text-indigo-400">Mister Trader</h1>
        <p className="text-slate-400 text-sm">Trading Journal</p>
      </div>
      
      <nav className="space-y-2">
        {navItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setCurrentPage(item.id)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
              currentPage === item.id
                ? 'bg-indigo-600 text-white'
                : 'text-slate-300 hover:bg-slate-800'
            }`}
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
      
      <div className="absolute bottom-6 left-6 right-6">
        <div className="bg-slate-800 rounded-lg p-4">
          <p className="text-sm text-slate-400">Tip of the day</p>
          <p className="text-xs text-slate-500 mt-1">
            Review your trading plan before each session.
          </p>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
