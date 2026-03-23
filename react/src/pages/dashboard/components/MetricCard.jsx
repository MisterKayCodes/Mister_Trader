import React from 'react';
import Icon from '../../../components/AppIcon';

const MetricCard = ({ title, value, change, changeType, icon, iconColor, loading }) => {
  const getChangeColor = () => {
    if (changeType === 'positive') return 'text-success';
    if (changeType === 'negative') return 'text-destructive';
    return 'text-muted-foreground';
  };

  const getChangeIcon = () => {
    if (changeType === 'positive') return 'TrendingUp';
    if (changeType === 'negative') return 'TrendingDown';
    return 'Minus';
  };

  if (loading) {
    return (
      <div className="bg-card border border-border rounded-lg p-4 md:p-6 animate-pulse">
        <div className="flex items-start justify-between mb-4">
          <div className="h-4 bg-muted rounded w-24"></div>
          <div className="w-10 h-10 bg-muted rounded-lg"></div>
        </div>
        <div className="h-8 bg-muted rounded w-32 mb-2"></div>
        <div className="h-4 bg-muted rounded w-20"></div>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6 hover-lift transition-smooth">
      <div className="flex items-start justify-between mb-4">
        <h3 className="text-sm md:text-base font-medium text-muted-foreground">{title}</h3>
        <div 
          className="w-10 h-10 md:w-12 md:h-12 rounded-lg flex items-center justify-center"
          style={{ backgroundColor: `${iconColor}15` }}
        >
          <Icon name={icon} size={20} color={iconColor} />
        </div>
      </div>
      
      <div className="mb-2">
        <p className="text-2xl md:text-3xl lg:text-4xl font-bold text-foreground data-text">
          {value}
        </p>
      </div>
      
      {change && (
        <div className={`flex items-center gap-1 ${getChangeColor()}`}>
          <Icon name={getChangeIcon()} size={16} />
          <span className="text-xs md:text-sm font-medium">{change}</span>
        </div>
      )}
    </div>
  );
};

export default MetricCard;