import React, { useState, useEffect } from 'react';
import analyticsApi from '../../../api/analytics';
import Icon from '../../../components/AppIcon';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const TimeTab = ({ selectedAccount }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [hourlyData, setHourlyData] = useState([]);

  useEffect(() => {
    fetchHourlyData();
  }, [selectedAccount]);

  const fetchHourlyData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsApi?.getHourly();
      const hourlyArray = [];
      if (data?.hourly && typeof data.hourly === 'object') {
         Object.entries(data.hourly).forEach(([hourStr, stats]) => {
            const hour = parseInt(hourStr, 10);
            const trades = stats.wins + stats.losses;
            if (trades > 0) {
               hourlyArray.push({
                  hour: `${hour.toString().padStart(2, '0')}:00`,
                  trades: trades,
                  winRate: Math.round((stats.wins / trades) * 100),
                  // Backend doesn't currently store hourly PnL so mock or set 0
                  profitLoss: 0 
               });
            }
         });
      }
      setHourlyData(hourlyArray);
    } catch (err) {
      setError(err?.response?.data?.message || 'Failed to load hourly data');
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
          onClick={fetchHourlyData}
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
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[1, 2, 3, 4]?.map((i) => (
            <div key={i} className="bg-card border border-border rounded-lg p-6 animate-pulse">
              <div className="h-6 bg-muted rounded w-1/2 mb-2"></div>
              <div className="h-4 bg-muted rounded w-full"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!hourlyData || hourlyData?.length === 0) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="Timer" size={48} className="mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No Time Data</h3>
        <p className="text-muted-foreground">No hourly trading data recorded yet</p>
      </div>
    );
  }

  const bestHour = hourlyData?.reduce((max, hour) => (hour?.profitLoss > max?.profitLoss ? hour : max), hourlyData?.[0]);
  const worstHour = hourlyData?.reduce((min, hour) => (hour?.profitLoss < min?.profitLoss ? hour : min), hourlyData?.[0]);
  const mostActiveHour = hourlyData?.reduce((max, hour) => (hour?.trades > max?.trades ? hour : max), hourlyData?.[0]);

  return (
    <div className="space-y-6">
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Hourly Performance</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={hourlyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="hour" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip
              contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
              labelStyle={{ color: '#f3f4f6' }}
            />
            <Bar dataKey="profitLoss" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-success/10 flex items-center justify-center">
              <Icon name="TrendingUp" size={20} className="text-success" />
            </div>
            <h4 className="text-sm font-medium text-muted-foreground">Best Hour</h4>
          </div>
          <p className="text-2xl font-bold text-foreground mb-1">{bestHour?.hour}</p>
          <p className="text-sm text-success">+${bestHour?.profitLoss?.toFixed(2)}</p>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-destructive/10 flex items-center justify-center">
              <Icon name="TrendingDown" size={20} className="text-destructive" />
            </div>
            <h4 className="text-sm font-medium text-muted-foreground">Worst Hour</h4>
          </div>
          <p className="text-2xl font-bold text-foreground mb-1">{worstHour?.hour}</p>
          <p className="text-sm text-destructive">${worstHour?.profitLoss?.toFixed(2)}</p>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
              <Icon name="Activity" size={20} className="text-primary" />
            </div>
            <h4 className="text-sm font-medium text-muted-foreground">Most Active</h4>
          </div>
          <p className="text-2xl font-bold text-foreground mb-1">{mostActiveHour?.hour}</p>
          <p className="text-sm text-muted-foreground">{mostActiveHour?.trades} trades</p>
        </div>
      </div>

      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Time-Based Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {hourlyData?.slice(0, 6)?.map((hour, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-muted/30 rounded-lg">
              <div>
                <p className="text-sm font-medium text-foreground">{hour?.hour}</p>
                <p className="text-xs text-muted-foreground">{hour?.trades} trades</p>
              </div>
              <div className="text-right">
                <p className={`text-sm font-semibold ${
                  hour?.profitLoss >= 0 ? 'text-success' : 'text-destructive'
                }`}>
                  {hour?.profitLoss >= 0 ? '+' : ''}${hour?.profitLoss?.toFixed(2)}
                </p>
                <p className="text-xs text-muted-foreground">{hour?.winRate}% win rate</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TimeTab;