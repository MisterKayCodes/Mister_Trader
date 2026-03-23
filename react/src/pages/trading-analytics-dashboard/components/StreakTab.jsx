import React, { useState, useEffect } from 'react';
import analyticsApi from '../../../api/analytics';
import Icon from '../../../components/AppIcon';

const StreakTab = ({ selectedAccount }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [streakData, setStreakData] = useState(null);

  useEffect(() => {
    fetchStreakData();
  }, [selectedAccount]);

  const fetchStreakData = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsApi?.getStats();
      if (data) {
         setStreakData({
           currentWinStreak: data.current_streak_type === 'WIN' ? data.current_streak : 0,
           currentLossStreak: data.current_streak_type === 'LOSS' ? data.current_streak : 0,
           longestWinStreak: data.best_win_streak || 0,
           longestLossStreak: data.worst_loss_streak || 0,
           avgWinStreak: 0,
           avgLossStreak: 0,
           streakRatio: data.worst_loss_streak > 0 ? (data.best_win_streak / data.worst_loss_streak) : (data.best_win_streak > 0 ? data.best_win_streak : 0)
         });
      } else {
         setStreakData(null);
      }
    } catch (err) {
      setError(err?.response?.data?.message || 'Failed to load streak data');
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
          onClick={fetchStreakData}
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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2]?.map((i) => (
            <div key={i} className="bg-card border border-border rounded-lg p-6 animate-pulse">
              <div className="h-8 bg-muted rounded w-1/2 mb-4"></div>
              <div className="h-16 bg-muted rounded w-full"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!streakData) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="Zap" size={48} className="mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No Streak Data</h3>
        <p className="text-muted-foreground">No streak data recorded yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-success/10 to-success/5 border border-success/20 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-lg bg-success/20 flex items-center justify-center">
              <Icon name="TrendingUp" size={24} className="text-success" />
            </div>
            <h3 className="text-lg font-semibold text-foreground">Winning Streak</h3>
          </div>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground mb-1">Current Streak</p>
              <p className="text-4xl font-bold text-success">{streakData?.currentWinStreak || 0}</p>
              <p className="text-xs text-muted-foreground mt-1">consecutive wins</p>
            </div>
            <div className="pt-4 border-t border-success/20">
              <p className="text-sm text-muted-foreground mb-1">Longest Streak</p>
              <p className="text-2xl font-bold text-foreground">{streakData?.longestWinStreak || 0}</p>
              <p className="text-xs text-muted-foreground mt-1">best performance</p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-destructive/10 to-destructive/5 border border-destructive/20 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-lg bg-destructive/20 flex items-center justify-center">
              <Icon name="TrendingDown" size={24} className="text-destructive" />
            </div>
            <h3 className="text-lg font-semibold text-foreground">Losing Streak</h3>
          </div>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground mb-1">Current Streak</p>
              <p className="text-4xl font-bold text-destructive">{streakData?.currentLossStreak || 0}</p>
              <p className="text-xs text-muted-foreground mt-1">consecutive losses</p>
            </div>
            <div className="pt-4 border-t border-destructive/20">
              <p className="text-sm text-muted-foreground mb-1">Longest Streak</p>
              <p className="text-2xl font-bold text-foreground">{streakData?.longestLossStreak || 0}</p>
              <p className="text-xs text-muted-foreground mt-1">worst drawdown</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
              <Icon name="Zap" size={20} className="text-primary" />
            </div>
            <h4 className="text-sm font-medium text-muted-foreground">Avg Win Streak</h4>
          </div>
          <p className="text-2xl font-bold text-foreground">{streakData?.avgWinStreak?.toFixed(1) || '0.0'}</p>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-warning/10 flex items-center justify-center">
              <Icon name="AlertTriangle" size={20} className="text-warning" />
            </div>
            <h4 className="text-sm font-medium text-muted-foreground">Avg Loss Streak</h4>
          </div>
          <p className="text-2xl font-bold text-foreground">{streakData?.avgLossStreak?.toFixed(1) || '0.0'}</p>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-info/10 flex items-center justify-center">
              <Icon name="BarChart3" size={20} className="text-info" />
            </div>
            <h4 className="text-sm font-medium text-muted-foreground">Streak Ratio</h4>
          </div>
          <p className="text-2xl font-bold text-foreground">
            {streakData?.streakRatio?.toFixed(2) || '0.00'}
          </p>
        </div>
      </div>

      <div className="bg-card border border-border rounded-lg p-6">
        <h3 className="text-lg font-semibold text-foreground mb-4">Streak Analysis</h3>
        <div className="space-y-3">
          <div className="flex items-start gap-2">
            <Icon name="CheckCircle" size={16} className="text-success mt-0.5" />
            <p className="text-sm text-muted-foreground">
              Your longest winning streak was <span className="font-semibold text-foreground">{streakData?.longestWinStreak || 0} trades</span>, showing strong consistency during peak performance.
            </p>
          </div>
          <div className="flex items-start gap-2">
            <Icon name="AlertCircle" size={16} className="text-warning mt-0.5" />
            <p className="text-sm text-muted-foreground">
              Your longest losing streak was <span className="font-semibold text-foreground">{streakData?.longestLossStreak || 0} trades</span>. Consider implementing stricter risk management during drawdowns.
            </p>
          </div>
          <div className="flex items-start gap-2">
            <Icon name="Info" size={16} className="text-primary mt-0.5" />
            <p className="text-sm text-muted-foreground">
              Current streak: {streakData?.currentWinStreak > 0 ? (
                <span className="font-semibold text-success">{streakData?.currentWinStreak} wins</span>
              ) : streakData?.currentLossStreak > 0 ? (
                <span className="font-semibold text-destructive">{streakData?.currentLossStreak} losses</span>
              ) : (
                <span className="font-semibold text-foreground">No active streak</span>
              )}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StreakTab;