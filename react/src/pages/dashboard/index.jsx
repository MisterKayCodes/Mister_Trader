import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import api from '../../auth/api'; // axios instance with auth

import AuthenticatedHeader from '../../components/layout/AuthenticatedHeader';
import PrimaryNavigation from '../../components/layout/PrimaryNavigation';
import AccountContextBar from '../../components/layout/AccountContextBar';
import MetricCard from './components/MetricCard';
import RecentTradesTable from './components/RecentTradesTable';
import PerformanceChart from './components/PerformanceChart';
import QuickActions from './components/QuickActions';
import TradingInsights from './components/TradingInsights';

const Dashboard = () => {
  const navigate = useNavigate();
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState({
    totalProfitLoss: 0,
    winRate: 0,
    avgTradeDuration: '',
    activePositions: 0,
    totalTrades: 0,
    winningTrades: 0,
    losingTrades: 0,
    bestWinStreak: 0,
    currentStreak: 0,
    currentStreakType: ''
  });
  const [recentTrades, setRecentTrades] = useState([]);
  const [performanceData, setPerformanceData] = useState([]);
  const [insights, setInsights] = useState([]);

  useEffect(() => {
    if (selectedAccount) {
      fetchDashboardData(selectedAccount);
    }
  }, [selectedAccount]);

  const fetchDashboardData = async (accountId) => {
    setLoading(true);

    try {
      // Fetch analytics stats
      const statsRes = await api.get('/analytics/stats', {
        params: { account_id: accountId }
      });
      const stats = statsRes.data;

      // Fetch recent trades
      const tradesRes = await api.get('/trades', {
        params: { account_id: accountId }
      });
      const trades = tradesRes.data;
      const recent = trades.slice(-5).reverse();

      // Map backend snake_case trade fields to table-friendly format
      const mappedTrades = recent.map(t => ({
        id: t.id,
        symbol: t.symbol,
        type: t.side === 'BUY' || t.side === 'LONG' ? 'Long' : 'Short',
        entryPrice: t.entry_price || 0,
        exitPrice: t.exit_price || 0,
        profitLoss: t.pnl || 0,
        exitDate: t.close_timestamp || t.open_timestamp || t.created_at,
        state: t.state,
        outcome: t.outcome
      }));

      // Build performance chart data from closed trades (cumulative PnL over time)
      const closedTrades = trades
        .filter(t => t.state === 'closed' && t.close_timestamp)
        .sort((a, b) => new Date(a.close_timestamp) - new Date(b.close_timestamp));

      let cumulativePnl = 0;
      const perfData = closedTrades.map(t => {
        cumulativePnl += (t.pnl || 0);
        const d = new Date(t.close_timestamp);
        return {
          date: d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          profit: Math.round(cumulativePnl * 100) / 100,
          balance: Math.round(cumulativePnl * 100) / 100
        };
      });

      // Fetch trading psychology insights and transform to component format
      let insightItems = [];
      try {
        const psychologyRes = await api.get('/analytics/psychology');
        const psychology = psychologyRes.data || {};

        // Convert backend insights (strings) into component format
        if (psychology.insights && psychology.insights.length > 0) {
          insightItems = psychology.insights.map((text, idx) => ({
            id: `insight-${idx}`,
            type: 'success',
            title: 'Psychology Insight',
            description: text
          }));
        }

        // Add emotion-based insights
        if (psychology.by_emotion && psychology.by_emotion.length > 0) {
          psychology.by_emotion.slice(0, 3).forEach((em, idx) => {
            insightItems.push({
              id: `emotion-${idx}`,
              type: em.win_rate >= 60 ? 'success' : em.win_rate >= 40 ? 'info' : 'warning',
              title: `${em.emotion} Trades`,
              description: `${em.win_rate}% win rate across ${em.trades} trades (P&L: $${em.pnl.toFixed(2)})`
            });
          });
        }

        // Add best combo insights
        if (psychology.best_combos && psychology.best_combos.length > 0) {
          psychology.best_combos.slice(0, 2).forEach((combo, idx) => {
            insightItems.push({
              id: `combo-${idx}`,
              type: combo.win_rate >= 60 ? 'success' : 'info',
              title: `${combo.emotion} + ${combo.symbol}`,
              description: `${combo.win_rate}% win rate over ${combo.trades} trades`
            });
          });
        }
      } catch (err) {
        console.warn('Psychology data not available:', err);
      }

      // Calculate avg trade duration from closed trades
      const avgDuration = calculateAvgTradeDuration(trades);

      // Calculate active positions - trades with state != closed
      const activePositionsCount = trades.filter(t => t.state !== 'closed').length;

      setMetrics({
        totalProfitLoss: stats.total_pnl || 0,
        winRate: stats.win_rate || 0,
        avgTradeDuration: avgDuration || 'N/A',
        activePositions: activePositionsCount,
        totalTrades: stats.total_trades || 0,
        winningTrades: stats.winning_trades || 0,
        losingTrades: stats.losing_trades || 0,
        bestWinStreak: stats.best_win_streak || 0,
        currentStreak: stats.current_streak || 0,
        currentStreakType: stats.current_streak_type || ''
      });

      setRecentTrades(mappedTrades);
      setPerformanceData(perfData);
      setInsights(insightItems);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    }

    setLoading(false);
  };

  const calculateAvgTradeDuration = (trades) => {
    if (!trades.length) return '';
    const closedTrades = trades.filter(t => t.state === 'closed' && t.open_timestamp && t.close_timestamp);
    if (!closedTrades.length) return '';

    const totalMs = closedTrades.reduce((acc, t) => {
      const openDate = new Date(t.open_timestamp);
      const closeDate = new Date(t.close_timestamp);
      return acc + (closeDate - openDate);
    }, 0);

    const avgMs = totalMs / closedTrades.length;
    const avgHours = avgMs / (1000 * 60 * 60);

    if (avgHours < 1) {
      const avgMinutes = avgMs / (1000 * 60);
      return `${avgMinutes.toFixed(0)} min`;
    } else if (avgHours < 24) {
      return `${avgHours.toFixed(1)} hrs`;
    } else {
      const avgDays = avgHours / 24;
      return `${avgDays.toFixed(1)} days`;
    }
  };

  const handleAccountChange = (accountId) => {
    setSelectedAccount(accountId);
  };

  const handleViewAllTrades = () => {
    navigate('/trades-management');
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(value);
  };

  // Derive smart change labels from real data
  const getPnlChangeType = () => {
    if (metrics.totalProfitLoss > 0) return 'positive';
    if (metrics.totalProfitLoss < 0) return 'negative';
    return 'neutral';
  };

  const getWinRateChangeType = () => {
    if (metrics.winRate >= 55) return 'positive';
    if (metrics.winRate < 45) return 'negative';
    return 'neutral';
  };

  return (
    <div className="min-h-screen bg-background">
      <AuthenticatedHeader />
      <PrimaryNavigation />
      <AccountContextBar onAccountChange={handleAccountChange} />
      <main className="main-content with-account-context">
        <div className="main-content-container">
          <div className="mb-6 md:mb-8">
            <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold text-foreground mb-2">
              Trading Dashboard
            </h1>
            <p className="text-sm md:text-base text-muted-foreground">
              Monitor your trading performance and key metrics
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
            <MetricCard
              title="Total P/L"
              value={formatCurrency(metrics?.totalProfitLoss)}
              change={`${metrics.winningTrades}W / ${metrics.losingTrades}L`}
              changeType={getPnlChangeType()}
              icon="DollarSign"
              iconColor="var(--color-success)"
              loading={loading}
            />
            <MetricCard
              title="Win Rate"
              value={`${metrics?.winRate.toFixed(1)}%`}
              change={`${metrics.totalTrades} total trades`}
              changeType={getWinRateChangeType()}
              icon="Target"
              iconColor="var(--color-primary)"
              loading={loading}
            />
            <MetricCard
              title="Avg Trade Duration"
              value={metrics?.avgTradeDuration}
              change={metrics.currentStreak > 0 ? `${metrics.currentStreak} ${metrics.currentStreakType} streak` : 'No active streak'}
              changeType={metrics.currentStreakType === 'WIN' ? 'positive' : metrics.currentStreakType === 'LOSS' ? 'negative' : 'neutral'}
              icon="Clock"
              iconColor="var(--color-accent)"
              loading={loading}
            />
            <MetricCard
              title="Active Positions"
              value={metrics?.activePositions}
              change={metrics.bestWinStreak > 0 ? `Best streak: ${metrics.bestWinStreak}W` : '—'}
              changeType="neutral"
              icon="TrendingUp"
              iconColor="var(--color-warning)"
              loading={loading}
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 md:gap-6 mb-6 md:mb-8">
            <div className="lg:col-span-2">
              <PerformanceChart data={performanceData} loading={loading} />
            </div>
            <div>
              <TradingInsights insights={insights} loading={loading} />
            </div>
          </div>

          <div className="mb-6 md:mb-8">
            <QuickActions />
          </div>

          <div>
            <RecentTradesTable
              trades={recentTrades}
              loading={loading}
              onViewAll={handleViewAllTrades}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
