import React, { useState, useEffect } from 'react';
import analyticsApi from '../../../api/analytics';
import MetricCard from '../../dashboard/components/MetricCard';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import Icon from '../../../components/AppIcon';

const OverviewTab = ({ selectedAccount }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchStats();
  }, [selectedAccount]);

  const fetchStats = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsApi?.getStats();
      setStats(data);
    } catch (err) {
      setError(err?.response?.data?.message || 'Failed to load statistics');
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
          onClick={fetchStats}
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
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4]?.map((i) => (
            <MetricCard 
              key={i} 
              loading={true}
              title=""
              value=""
              change={0}
              changeType="positive"
              icon="BarChart3"
              iconColor="#000000"
            />
          ))}
        </div>
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="h-64 bg-muted rounded animate-pulse"></div>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="BarChart3" size={48} className="mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No Data Available</h3>
        <p className="text-muted-foreground">Start trading to see your analytics</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Total P&L"
          value={`$${stats?.totalProfitLoss?.toLocaleString() || '0'}`}
          change={stats?.profitLossChange}
          changeType={stats?.totalProfitLoss >= 0 ? 'positive' : 'negative'}
          icon="DollarSign"
          iconColor="#10b981"
        />
        <MetricCard
          title="Win Rate"
          value={`${stats?.winRate || 0}%`}
          change={stats?.winRateChange}
          changeType={stats?.winRate >= 50 ? 'positive' : 'negative'}
          icon="Target"
          iconColor="#3b82f6"
        />
        <MetricCard
          title="Total Trades"
          value={stats?.totalTrades || 0}
          change={stats?.tradesChange}
          changeType="positive"
          icon="TrendingUp"
          iconColor="#8b5cf6"
        />
        <MetricCard
          title="Avg Trade"
          value={`$${stats?.avgTrade?.toLocaleString() || '0'}`}
          change={stats?.avgTradeChange}
          changeType={stats?.avgTrade >= 0 ? 'positive' : 'negative'}
          icon="BarChart3"
          iconColor="#f59e0b"
        />
      </div>

      {stats?.chartData && (
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Performance Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={stats?.chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="date" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                labelStyle={{ color: '#f3f4f6' }}
              />
              <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default OverviewTab;