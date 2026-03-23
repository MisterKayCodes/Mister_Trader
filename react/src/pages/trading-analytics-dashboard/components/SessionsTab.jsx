import React, { useState, useEffect } from 'react';
import analyticsApi from '../../../api/analytics';
import Icon from '../../../components/AppIcon';

const SessionsTab = ({ selectedAccount }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetchSessions();
  }, [selectedAccount]);

  const fetchSessions = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsApi?.getSessions();
      
      // The backend returns { sessions: { "London": 50.0, ... }, details: { london: { wins: 0, losses: 0 } } }
      // We must map this dictionary into an array structure for the UI to consume.
      const sessionArray = [];
      if (data?.sessions && typeof data.sessions === 'object') {
        Object.entries(data.sessions).forEach(([name, winRate]) => {
           const detailKey = name.toLowerCase().replace(' ', '');
           const details = data?.details?.[detailKey] || { wins: 0, losses: 0 };
           const trades = details.wins + details.losses;
           sessionArray.push({
              name,
              winRate,
              trades,
              wins: details.wins,
              losses: details.losses,
              // The backend doesn't currently provide individual session PnL or duration so we omit those or set 0
              profitLossAmount: 0, 
              profitLoss: 0
           });
        });
      }
      setSessions(sessionArray);
    } catch (err) {
      setError(err?.response?.data?.message || 'Failed to load sessions data');
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
          onClick={fetchSessions}
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
      <div className="space-y-4">
        {[1, 2, 3]?.map((i) => (
          <div key={i} className="bg-card border border-border rounded-lg p-6 animate-pulse">
            <div className="h-6 bg-muted rounded w-1/3 mb-4"></div>
            <div className="space-y-2">
              <div className="h-4 bg-muted rounded w-full"></div>
              <div className="h-4 bg-muted rounded w-2/3"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (!sessions || sessions?.length === 0) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="Clock" size={48} className="mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No Sessions Data</h3>
        <p className="text-muted-foreground">No trading sessions recorded yet</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {sessions?.map((session, index) => (
        <div key={index} className="bg-card border border-border rounded-lg p-6 hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h3 className="text-lg font-semibold text-foreground">{session?.name || `Session ${index + 1}`}</h3>
              <p className="text-sm text-muted-foreground">{session?.date}</p>
            </div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              session?.profitLoss >= 0 ? 'bg-success/10 text-success' : 'bg-destructive/10 text-destructive'
            }`}>
              {session?.profitLoss >= 0 ? '+' : ''}{session?.profitLoss?.toFixed(2)}%
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-xs text-muted-foreground mb-1">Trades</p>
              <p className="text-lg font-semibold text-foreground">{session?.trades || 0}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground mb-1">Win Rate</p>
              <p className="text-lg font-semibold text-foreground">{session?.winRate || 0}%</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground mb-1">Wins / Losses</p>
              <p className="text-lg font-semibold text-foreground">{session?.wins}W / {session?.losses}L</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default SessionsTab;