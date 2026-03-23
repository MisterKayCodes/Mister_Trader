import React, { useState, useEffect } from 'react';
import analyticsApi from '../../../api/analytics';
import Icon from '../../../components/AppIcon';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const PsychologyTab = ({ selectedAccount }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [psychology, setPsychology] = useState(null);

  useEffect(() => {
    fetchPsychology();
  }, [selectedAccount]);

  const fetchPsychology = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsApi?.getPsychology();
      // The backend returns: { by_emotion: [], best_combos: [], insights: [] }
      if (data && data.by_emotion) {
         // Create emotionDistribution for the Pie chart
         const emotionDistribution = data.by_emotion.map(e => ({
            name: e.emotion,
            value: e.trades || 1
         }));
         setPsychology({
            ...data,
            emotionDistribution
         });
      } else {
         setPsychology(data);
      }
    } catch (err) {
      setError(err?.response?.data?.message || 'Failed to load psychology data');
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  if (error) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="AlertCircle" size={48} className="mx-auto mb-4 text-destructive" />
        <h3 className="text-lg font-semibold text-foreground mb-2">Error Loading Data</h3>
        <p className="text-muted-foreground mb-4">{error}</p>
        <button
          onClick={fetchPsychology}
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
      </div>
    );
  }

  if (!psychology || (!psychology.by_emotion?.length && !psychology.insights?.length)) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 text-center">
        <Icon name="Brain" size={48} className="mx-auto mb-4 text-muted-foreground" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No Psychology Data</h3>
        <p className="text-muted-foreground">No psychological trading data recorded yet. Wait for enough closed trades with logged pre-trade emotions.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {psychology?.emotionDistribution?.length > 0 && (
            <div className="bg-card border border-border rounded-lg p-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">Emotion Frequency</h3>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={psychology?.emotionDistribution}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100)?.toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {psychology?.emotionDistribution?.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS?.[index % COLORS?.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}

          <div className="bg-card border border-border rounded-lg p-6 overflow-x-auto">
              <h3 className="text-lg font-semibold text-foreground mb-4">Emotion Performance</h3>
              <table className="w-full text-sm">
                 <thead>
                    <tr className="border-b border-border text-left">
                       <th className="pb-2 text-muted-foreground">Emotion</th>
                       <th className="pb-2 text-muted-foreground">Trades</th>
                       <th className="pb-2 text-muted-foreground">Win Rate</th>
                       <th className="pb-2 text-muted-foreground">PnL</th>
                    </tr>
                 </thead>
                 <tbody>
                    {psychology?.by_emotion?.map((e, idx) => (
                       <tr key={idx} className="border-b border-border">
                          <td className="py-3 font-medium capitalize">{e.emotion}</td>
                          <td className="py-3">{e.trades}</td>
                          <td className={`py-3 font-medium ${e.win_rate >= 50 ? 'text-success' : 'text-destructive'}`}>{e.win_rate}%</td>
                          <td className={`py-3 font-medium ${e.pnl >= 0 ? 'text-success' : 'text-destructive'}`}>
                             {e.pnl >= 0 ? '+' : ''}${e.pnl}
                          </td>
                       </tr>
                    ))}
                 </tbody>
              </table>
          </div>
      </div>

      {(psychology?.best_combos?.length > 0 || psychology?.insights?.length > 0) && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {psychology?.insights?.length > 0 && (
                <div className="bg-card border border-border rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-foreground mb-4">Psychological Insights</h3>
                  <ul className="space-y-4">
                    {psychology?.insights?.map((insight, index) => (
                      <li key={index} className="flex items-start gap-3 bg-primary/5 p-3 rounded-md">
                        <Icon name="Lightbulb" size={20} className="text-primary mt-0.5 flex-shrink-0" />
                        <span className="text-sm font-medium text-foreground">{insight}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {psychology?.best_combos?.length > 0 && (
                 <div className="bg-card border border-border rounded-lg p-6">
                   <h3 className="text-lg font-semibold text-foreground mb-4">Best Performing Combos</h3>
                   <div className="space-y-3">
                     {psychology?.best_combos?.map((combo, index) => (
                        <div key={index} className="flex justify-between items-center p-3 bg-muted/30 rounded-md">
                           <div className="flex flex-col">
                              <span className="text-sm font-semibold text-foreground">{combo.symbol} + {combo.emotion}</span>
                              <span className="text-xs text-muted-foreground">{combo.trades} Trades</span>
                           </div>
                           <div className="flex flex-col text-right">
                              <span className="text-sm font-bold text-success">{combo.win_rate}% Win Rate</span>
                              <span className="text-xs text-muted-foreground">${combo.pnl} PnL</span>
                           </div>
                        </div>
                     ))}
                   </div>
                 </div>
              )}
          </div>
      )}
    </div>
  );
};

export default PsychologyTab;