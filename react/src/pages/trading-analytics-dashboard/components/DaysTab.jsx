import React, { useState, useEffect } from 'react';
import analyticsApi from '../../../api/analytics';
import Icon from '../../../components/AppIcon';

const DaysTab = ({ selectedAccount }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [days, setDays] = useState([]);

  useEffect(() => {
    fetchDays();
  }, [selectedAccount]);

  const fetchDays = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsApi?.getDays();
      // data.days is a dictionary like { "Monday": { pnl: 100, ... } }
      const daysArray = [];
      if (data?.days && typeof data.days === 'object') {
         Object.entries(data.days).forEach(([dayName, stats]) => {
            daysArray.push({
               day: dayName.substring(0, 3), // "Mon"
               date: dayName, // e.g. "Monday"
               profitLoss: stats.pnl,
               wins: stats.wins,
               losses: stats.losses,
               total: stats.total
            });
         });
      }
      setDays(daysArray);
    } catch (err) {
      setError(err?.response?.data?.message || 'Failed to load days data');
    } finally {
      setLoading(false);
    }
  };

  const getDayColor = (profitLoss) => {
    if (profitLoss > 0) return 'bg-success/20 border-success';
    if (profitLoss < 0) return 'bg-destructive/20 border-destructive';
    return 'bg-muted border-border';
  };

  if (error) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="AlertCircle" size={48} className="mx-auto mb-4 text-destructive" />
        <h3 className="text-lg font-semibold text-foreground mb-2">Error Loading Data</h3>
        <p className="text-muted-foreground mb-4">{error}</p>
        <button
          onClick={fetchDays}
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
      <div className="bg-card border border-border rounded-lg p-6">
        <div className="grid grid-cols-7 gap-2">
          {Array.from({ length: 35 })?.map((_, i) => (
            <div key={i} className="aspect-square bg-muted rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  if (!days || days?.length === 0) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="Calendar" size={48} className="mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No Days Data</h3>
        <p className="text-muted-foreground">No daily trading data recorded yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Daily Performance Calendar</h3>
        <div className="grid grid-cols-7 gap-2 mb-4">
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']?.map((day) => (
            <div key={day} className="text-center text-xs font-medium text-muted-foreground py-2">
              {day}
            </div>
          ))}
        </div>
        <div className="grid grid-cols-7 gap-2">
          {days?.map((day, index) => (
            <div
              key={index}
              className={`aspect-square border rounded-lg p-2 flex flex-col items-center justify-center hover:shadow-md transition-shadow cursor-pointer ${
                getDayColor(day?.profitLoss)
              }`}
              title={`${day?.date}: ${day?.profitLoss >= 0 ? '+' : ''}$${day?.profitLoss?.toFixed(2)}`}
            >
              <span className="text-xs font-medium text-foreground">{day?.day}</span>
              <span className={`text-xs font-semibold mt-1 ${
                day?.profitLoss >= 0 ? 'text-success' : 'text-destructive'
              }`}>
                {day?.profitLoss >= 0 ? '+' : ''}{day?.profitLoss?.toFixed(0)}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-success/10 flex items-center justify-center">
              <Icon name="TrendingUp" size={20} className="text-success" />
            </div>
            <h4 className="text-sm font-medium text-muted-foreground">Best Day</h4>
          </div>
          <p className="text-2xl font-bold text-success">+${days?.reduce((max, day) => Math.max(max, day?.profitLoss || 0), 0)?.toFixed(2)}</p>
        </div>
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-destructive/10 flex items-center justify-center">
              <Icon name="TrendingDown" size={20} className="text-destructive" />
            </div>
            <h4 className="text-sm font-medium text-muted-foreground">Worst Day</h4>
          </div>
          <p className="text-2xl font-bold text-destructive">${days?.reduce((min, day) => Math.min(min, day?.profitLoss || 0), 0)?.toFixed(2)}</p>
        </div>
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
              <Icon name="BarChart3" size={20} className="text-primary" />
            </div>
            <h4 className="text-sm font-medium text-muted-foreground">Avg Day</h4>
          </div>
          <p className="text-2xl font-bold text-foreground">
            ${(days?.reduce((sum, day) => sum + (day?.profitLoss || 0), 0) / days?.length)?.toFixed(2)}
          </p>
        </div>
      </div>
    </div>
  );
};

export default DaysTab;