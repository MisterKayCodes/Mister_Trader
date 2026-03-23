import React, { useState, useEffect } from 'react';
import analyticsApi from '../../../api/analytics';
import Icon from '../../../components/AppIcon';

const PairsTab = ({ selectedAccount }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pairs, setPairs] = useState([]);

  useEffect(() => {
    fetchPairs();
  }, [selectedAccount]);

  const fetchPairs = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsApi?.getSymbols();
      const mapped = (data?.symbols || []).map(s => ({
         symbol: s.symbol,
         trades: s.trades,
         winRate: s.win_rate,
         profitLoss: s.pnl,
         avgTrade: s.trades > 0 ? s.pnl / s.trades : 0
      }));
      setPairs(mapped);
    } catch (err) {
      setError(err?.response?.data?.message || 'Failed to load pairs data');
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
          onClick={fetchPairs}
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
      <div className="bg-card border border-border rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-left"><div className="h-4 bg-muted rounded w-20"></div></th>
                <th className="px-6 py-3 text-left"><div className="h-4 bg-muted rounded w-16"></div></th>
                <th className="px-6 py-3 text-left"><div className="h-4 bg-muted rounded w-20"></div></th>
                <th className="px-6 py-3 text-left"><div className="h-4 bg-muted rounded w-16"></div></th>
                <th className="px-6 py-3 text-left"><div className="h-4 bg-muted rounded w-24"></div></th>
              </tr>
            </thead>
            <tbody>
              {[1, 2, 3, 4, 5]?.map((i) => (
                <tr key={i} className="border-t border-border animate-pulse">
                  <td className="px-6 py-4"><div className="h-4 bg-muted rounded w-16"></div></td>
                  <td className="px-6 py-4"><div className="h-4 bg-muted rounded w-12"></div></td>
                  <td className="px-6 py-4"><div className="h-4 bg-muted rounded w-16"></div></td>
                  <td className="px-6 py-4"><div className="h-4 bg-muted rounded w-12"></div></td>
                  <td className="px-6 py-4"><div className="h-4 bg-muted rounded w-20"></div></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  }

  if (!pairs || pairs?.length === 0) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="TrendingUp" size={48} className="mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No Pairs Data</h3>
        <p className="text-muted-foreground">No trading pairs recorded yet</p>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Symbol</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Trades</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Win Rate</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Avg Trade</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Total P&L</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {pairs?.map((pair, index) => (
              <tr key={index} className="hover:bg-muted/30 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                      <Icon name="TrendingUp" size={16} className="text-primary" />
                    </div>
                    <span className="text-sm font-semibold text-foreground">{pair?.symbol}</span>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{pair?.trades || 0}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`text-sm font-medium ${
                    pair?.winRate >= 50 ? 'text-success' : 'text-destructive'
                  }`}>
                    {pair?.winRate || 0}%
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">${pair?.avgTrade?.toLocaleString() || '0'}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`text-sm font-semibold ${
                    pair?.profitLoss >= 0 ? 'text-success' : 'text-destructive'
                  }`}>
                    {pair?.profitLoss >= 0 ? '+' : ''}${pair?.profitLoss?.toLocaleString() || '0'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PairsTab;