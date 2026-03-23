import React from 'react';
import Icon from '../../../components/AppIcon';

const TradingInsights = ({ insights = [], loading }) => {
  const getInsightIcon = (type) => {
    switch (type) {
      case 'success':
        return { name: 'CheckCircle2', color: 'var(--color-success)' };
      case 'warning':
        return { name: 'AlertTriangle', color: 'var(--color-warning)' };
      case 'info':
        return { name: 'Info', color: 'var(--color-primary)' };
      default:
        return { name: 'Lightbulb', color: 'var(--color-accent)' };
    }
  };

  if (loading) {
    return (
      <div className="bg-card border border-border rounded-lg p-4 md:p-6">
        <div className="h-6 bg-muted rounded w-32 mb-4"></div>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-20 bg-muted rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6">
      <div className="flex items-center gap-2 mb-4">
        <Icon name="Sparkles" size={20} className="text-accent" />
        <h2 className="text-lg md:text-xl font-semibold text-foreground">Trading Insights</h2>
      </div>
      <div className="space-y-3">
        {Array.isArray(insights) && insights.length > 0 ? (
          insights.map((insight) => {
            const iconData = getInsightIcon(insight?.type);
            return (
              <div
                key={insight?.id}
                className="flex items-start gap-3 p-3 md:p-4 rounded-lg border border-border hover:border-primary/30 transition-smooth"
              >
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                  style={{ backgroundColor: `${iconData?.color}15` }}
                >
                  <Icon name={iconData?.name} size={20} color={iconData?.color} />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm md:text-base font-medium text-foreground mb-1">
                    {insight?.title}
                  </h3>
                  <p className="text-xs md:text-sm text-muted-foreground line-clamp-2">
                    {insight?.description}
                  </p>
                </div>
              </div>
            );
          })
        ) : (
          <div className="text-center py-8">
            <Icon name="Sparkles" size={48} className="mx-auto mb-4 text-muted-foreground opacity-50" />
            <p className="text-muted-foreground text-sm">No insights available yet</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TradingInsights;
