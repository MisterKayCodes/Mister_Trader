import React from 'react';
import Icon from '../../../components/AppIcon';
import TradeVoiceNotes from './TradeVoiceNotes';

const TradeReferencePanel = ({ tradeData }) => {
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
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const profitLoss = tradeData?.pnl !== undefined ? tradeData.pnl : tradeData?.profitLoss;
  const profitLossColor = profitLoss >= 0 ? 'text-success' : 'text-error';
  const profitLossIcon = profitLoss >= 0 ? 'TrendingUp' : 'TrendingDown';
  const side = tradeData?.side?.toUpperCase() || tradeData?.direction?.toUpperCase();
  const entryPrice = tradeData?.entry_price || tradeData?.entryPrice;
  const exitPrice = tradeData?.exit_price || tradeData?.exitPrice;
  const entryTime = tradeData?.open_timestamp || tradeData?.entryTime;
  const exitTime = tradeData?.close_timestamp || tradeData?.exitTime;
  const returnPercentage = tradeData?.return_percentage || tradeData?.returnPercentage;

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6 space-y-4 md:space-y-6 overflow-hidden">
      <div className="flex items-center justify-between">
        <h3 className="text-base md:text-lg font-semibold text-foreground">Trade Reference</h3>
        <span className={`flex items-center gap-1 text-sm md:text-base font-semibold ${profitLossColor}`}>
          <Icon name={profitLossIcon} size={18} />
          {formatCurrency(profitLoss)}
        </span>
      </div>
      <div className="space-y-3 md:space-y-4">
        <div className="flex items-center justify-between py-2 border-b border-border">
          <span className="text-xs md:text-sm text-muted-foreground">Symbol</span>
          <span className="text-sm md:text-base font-medium text-foreground">{tradeData?.symbol}</span>
        </div>

        <div className="flex items-center justify-between py-2 border-b border-border">
          <span className="text-xs md:text-sm text-muted-foreground">Direction</span>
          <span className={`text-sm md:text-base font-medium ${side === 'BUY' || side === 'LONG' ? 'text-success' : 'text-error'}`}>
            {side}
          </span>
        </div>

        <div className="flex items-center justify-between py-2 border-b border-border">
          <span className="text-xs md:text-sm text-muted-foreground">Entry Price</span>
          <span className="text-sm md:text-base font-medium text-foreground">{formatCurrency(entryPrice)}</span>
        </div>

        <div className="flex items-center justify-between py-2 border-b border-border">
          <span className="text-xs md:text-sm text-muted-foreground">Exit Price</span>
          <span className="text-sm md:text-base font-medium text-foreground">{formatCurrency(exitPrice)}</span>
        </div>

        <div className="flex items-center justify-between py-2 border-b border-border">
          <span className="text-xs md:text-sm text-muted-foreground">Quantity</span>
          <span className="text-sm md:text-base font-medium text-foreground">{tradeData?.quantity}</span>
        </div>

        <div className="flex items-center justify-between py-2 border-b border-border">
          <span className="text-xs md:text-sm text-muted-foreground">Entry Time</span>
          <span className="text-xs md:text-sm text-foreground">{formatDate(entryTime)}</span>
        </div>

        <div className="flex items-center justify-between py-2">
          <span className="text-xs md:text-sm text-muted-foreground">Exit Time</span>
          <span className="text-xs md:text-sm text-foreground">{formatDate(exitTime)}</span>
        </div>
      </div>
      <div className="pt-3 md:pt-4 border-t border-border">
        <div className="flex items-center justify-between">
          <span className="text-xs md:text-sm font-medium text-muted-foreground">Return %</span>
          <span className={`text-base md:text-lg font-semibold ${profitLossColor}`}>
            {returnPercentage > 0 ? '+' : ''}{returnPercentage?.toFixed(2)}%
          </span>
        </div>
      </div>
      
      {/* Voice Notes Section */}
      <TradeVoiceNotes tradeId={tradeData?.id} />
    </div>
  );
};

export default TradeReferencePanel;