import React, { useState, useEffect } from 'react';
import analyticsApi from '../../../api/analytics';
import Icon from '../../../components/AppIcon';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const StrategiesTab = ({ selectedAccount }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [strategies, setStrategies] = useState([]);

  useEffect(() => {
    fetchStrategies();
  }, [selectedAccount]);

  const fetchStrategies = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsApi?.getStrategies();
      const mapped = (data?.strategies || []).map(s => ({
         name: s.name,
         trades: s.trades,
         winRate: s.win_rate,
         profitLoss: s.total_pnl,
         avgTrade: s.trades > 0 ? s.total_pnl / s.trades : 0
      }));
      setStrategies(mapped);
    } catch (err) {
      setError(err?.response?.data?.message || 'Failed to load strategies data');
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="AlertCircle" size={48} className="mx-auto mb-4 text-destructive" />
        <h3 className="text-lg font-semibold text-foreground mb-2">Error Loading Data</h3>
        <p className="text-muted-foreground mb-4">{error}</p>
        <button
          onClick={fetchStrategies}
          className="inline-flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
        >
          <Icon name="RefreshCw" size={16} />
          Retry
        </button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="h-64 bg-muted rounded animate-pulse"></div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[1, 2]?.map((i) => (
            <div key={i} className="bg-card border border-border rounded-lg p-6 animate-pulse">
              <div className="h-6 bg-muted rounded w-1/2 mb-4"></div>
              <div className="h-4 bg-muted rounded w-full"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!strategies || strategies?.length === 0) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="Target" size={48} className="mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No Strategies Data</h3>
        <p className="text-muted-foreground">No trading strategies recorded yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Strategy Performance Comparison</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={strategies}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="name" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip
              contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
              labelStyle={{ color: '#f3f4f6' }}
            />
            <Legend />
            <Bar dataKey="winRate" fill="#3b82f6" name="Win Rate (%)" />
            <Bar dataKey="profitLoss" fill="#10b981" name="P&L ($)" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {strategies?.map((strategy, index) => (
          <div key={index} className="bg-card border border-border rounded-lg p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <Icon name="Target" size={20} className="text-primary" />
              </div>
              <h3 className="text-lg font-semibold text-foreground">{strategy?.name}</h3>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Trades</span>
                <span className="text-sm font-semibold text-foreground">{strategy?.trades || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Win Rate</span>
                <span className="text-sm font-semibold text-foreground">{strategy?.winRate || 0}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">P&L</span>
                <span className={`text-sm font-semibold ${
                  strategy?.profitLoss >= 0 ? 'text-success' : 'text-destructive'
                }`}>
                  ${strategy?.profitLoss?.toLocaleString() || '0'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Avg Trade</span>
                <span className="text-sm font-semibold text-foreground">${strategy?.avgTrade?.toLocaleString() || '0'}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StrategiesTab;