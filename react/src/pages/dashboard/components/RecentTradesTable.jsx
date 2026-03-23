import React from 'react';
import Icon from '../../../components/AppIcon';

const RecentTradesTable = ({ trades, loading, onViewAll }) => {
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    })?.format(value);
  };

  const formatDate = (dateString) => {
    return new Date(dateString)?.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const getProfitColor = (profit) => {
    return profit >= 0 ? 'text-success' : 'text-destructive';
  };

  if (loading) {
    return (
      <div className="bg-card border border-border rounded-lg p-4 md:p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="h-6 bg-muted rounded w-32"></div>
          <div className="h-9 bg-muted rounded w-24"></div>
        </div>
        <div className="space-y-4">
          {[1, 2, 3, 4, 5]?.map((i) => (
            <div key={i} className="h-16 bg-muted rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg md:text-xl font-semibold text-foreground">Recent Trades</h2>
        <button
          onClick={onViewAll}
          className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary hover:bg-accent/10 rounded-lg transition-smooth"
        >
          <span>View All</span>
          <Icon name="ArrowRight" size={16} />
        </button>
      </div>
      <div className="overflow-x-auto scrollbar-custom">
        <table className="w-full min-w-[600px]">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left py-3 px-2 text-xs md:text-sm font-medium text-muted-foreground">Symbol</th>
              <th className="text-left py-3 px-2 text-xs md:text-sm font-medium text-muted-foreground">Type</th>
              <th className="text-right py-3 px-2 text-xs md:text-sm font-medium text-muted-foreground">Entry</th>
              <th className="text-right py-3 px-2 text-xs md:text-sm font-medium text-muted-foreground">Exit</th>
              <th className="text-right py-3 px-2 text-xs md:text-sm font-medium text-muted-foreground">P/L</th>
              <th className="text-left py-3 px-2 text-xs md:text-sm font-medium text-muted-foreground">Date</th>
            </tr>
          </thead>
          <tbody>
            {trades?.map((trade) => (
              <tr key={trade?.id} className="border-b border-border hover:bg-muted/50 transition-smooth">
                <td className="py-4 px-2">
                  <div className="flex items-center gap-2">
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                      trade?.type === 'Long' ? 'bg-success/10' : 'bg-destructive/10'
                    }`}>
                      <Icon 
                        name={trade?.type === 'Long' ? 'TrendingUp' : 'TrendingDown'} 
                        size={16} 
                        color={trade?.type === 'Long' ? 'var(--color-success)' : 'var(--color-destructive)'}
                      />
                    </div>
                    <span className="text-sm md:text-base font-medium text-foreground">{trade?.symbol}</span>
                  </div>
                </td>
                <td className="py-4 px-2">
                  <span className={`inline-flex px-2 py-1 text-xs font-medium rounded ${
                    trade?.type === 'Long' ?'bg-success/10 text-success' :'bg-destructive/10 text-destructive'
                  }`}>
                    {trade?.type}
                  </span>
                </td>
                <td className="py-4 px-2 text-right text-sm md:text-base text-foreground data-text">
                  {formatCurrency(trade?.entryPrice)}
                </td>
                <td className="py-4 px-2 text-right text-sm md:text-base text-foreground data-text">
                  {formatCurrency(trade?.exitPrice)}
                </td>
                <td className="py-4 px-2 text-right">
                  <span className={`text-sm md:text-base font-semibold data-text ${getProfitColor(trade?.profitLoss)}`}>
                    {formatCurrency(trade?.profitLoss)}
                  </span>
                </td>
                <td className="py-4 px-2 text-sm md:text-base text-muted-foreground">
                  {formatDate(trade?.exitDate)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {trades?.length === 0 && (
        <div className="text-center py-12">
          <Icon name="TrendingUp" size={48} className="mx-auto mb-4 text-muted-foreground opacity-50" />
          <p className="text-muted-foreground">No recent trades found</p>
        </div>
      )}
    </div>
  );
};

export default RecentTradesTable;