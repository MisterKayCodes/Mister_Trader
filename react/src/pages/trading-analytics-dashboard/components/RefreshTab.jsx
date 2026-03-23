import React, { useState } from 'react';
import analyticsApi from '../../../api/analytics';
import Icon from '../../../components/AppIcon';

const RefreshTab = () => {
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [lastRefresh, setLastRefresh] = useState(null);

  const handleRefresh = async () => {
    setLoading(true);
    setError(null);
    setSuccess(false);
    try {
      const response = await analyticsApi?.refreshAnalytics();
      setSuccess(true);
      setLastRefresh(new Date()?.toLocaleString());
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError(err?.response?.data?.message || 'Failed to refresh analytics');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-primary/10 flex items-center justify-center">
          <Icon name="RefreshCw" size={32} className="text-primary" />
        </div>
        
        <h2 className="text-2xl font-bold text-foreground mb-2">Refresh Analytics</h2>
        <p className="text-muted-foreground mb-6">
          Recalculate all analytics data based on your latest trades and performance metrics.
        </p>

        {error && (
          <div className="mb-6 p-4 bg-destructive/10 border border-destructive/20 rounded-lg flex items-center gap-3">
            <Icon name="AlertCircle" size={20} className="text-destructive" />
            <p className="text-sm text-destructive">{error}</p>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 bg-success/10 border border-success/20 rounded-lg flex items-center gap-3">
            <Icon name="CheckCircle" size={20} className="text-success" />
            <p className="text-sm text-success">Analytics refreshed successfully!</p>
          </div>
        )}

        <button
          onClick={handleRefresh}
          disabled={loading}
          className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <Icon name="Loader2" size={20} className="animate-spin" />
              Refreshing...
            </>
          ) : (
            <>
              <Icon name="RefreshCw" size={20} />
              Refresh Analytics
            </>
          )}
        </button>

        {lastRefresh && (
          <p className="mt-4 text-xs text-muted-foreground">
            Last refreshed: {lastRefresh}
          </p>
        )}
      </div>

      <div className="mt-6 bg-muted/30 border border-border rounded-lg p-6">
        <h3 className="text-sm font-semibold text-foreground mb-3">What gets refreshed?</h3>
        <ul className="space-y-2">
          <li className="flex items-start gap-2">
            <Icon name="CheckCircle" size={16} className="text-primary mt-0.5" />
            <span className="text-sm text-muted-foreground">Overall statistics and performance metrics</span>
          </li>
          <li className="flex items-start gap-2">
            <Icon name="CheckCircle" size={16} className="text-primary mt-0.5" />
            <span className="text-sm text-muted-foreground">Session-based performance analysis</span>
          </li>
          <li className="flex items-start gap-2">
            <Icon name="CheckCircle" size={16} className="text-primary mt-0.5" />
            <span className="text-sm text-muted-foreground">Strategy performance comparisons</span>
          </li>
          <li className="flex items-start gap-2">
            <Icon name="CheckCircle" size={16} className="text-primary mt-0.5" />
            <span className="text-sm text-muted-foreground">Symbol/pair profitability data</span>
          </li>
          <li className="flex items-start gap-2">
            <Icon name="CheckCircle" size={16} className="text-primary mt-0.5" />
            <span className="text-sm text-muted-foreground">Daily and hourly performance breakdowns</span>
          </li>
          <li className="flex items-start gap-2">
            <Icon name="CheckCircle" size={16} className="text-primary mt-0.5" />
            <span className="text-sm text-muted-foreground">Psychological trading patterns</span>
          </li>
          <li className="flex items-start gap-2">
            <Icon name="CheckCircle" size={16} className="text-primary mt-0.5" />
            <span className="text-sm text-muted-foreground">Winning and losing streak calculations</span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default RefreshTab;