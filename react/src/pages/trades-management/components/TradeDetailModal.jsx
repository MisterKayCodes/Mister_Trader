import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const TradeDetailModal = ({ isOpen, onClose, trade, onEdit }) => {
  if (!isOpen || !trade) return null;

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '—';
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const getProfitLossColor = (value) => {
    if (value > 0) return 'text-success';
    if (value < 0) return 'text-destructive';
    return 'text-muted-foreground';
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      open: { bg: 'bg-warning/10', text: 'text-warning', label: 'Open', icon: 'TrendingUp' },
      closed: { bg: 'bg-success/10', text: 'text-success', label: 'Closed', icon: 'CheckCircle' },
      pending: { bg: 'bg-muted', text: 'text-muted-foreground', label: 'Pending', icon: 'Clock' },
    };

    const config = statusConfig[status] || statusConfig.pending;
    return (
      <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${config.bg}`}>
        <Icon name={config.icon} size={18} className={config.text} />
        <span className={`text-sm font-medium ${config.text}`}>{config.label}</span>
      </div>
    );
  };

  const calculateDuration = () => {
    if (!trade.exitDate) return 'Ongoing';
    const entry = new Date(trade.entryDate);
    const exit = new Date(trade.exitDate);
    const days = Math.ceil((exit - entry) / (1000 * 60 * 60 * 24));
    return `${days} ${days === 1 ? 'day' : 'days'}`;
  };

  const calculateReturnPercentage = () => {
    if (!trade.exitPrice) return null;
    const returnPct =
      trade.type === 'long'
        ? ((trade.exitPrice - trade.entryPrice) / trade.entryPrice) * 100
        : ((trade.entryPrice - trade.exitPrice) / trade.entryPrice) * 100;
    return returnPct.toFixed(2);
  };

  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm">
      <div className="bg-card border border-border rounded-lg w-full max-w-3xl max-h-[90vh] overflow-y-auto scrollbar-custom">
        <div className="sticky top-0 bg-card border-b border-border px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <h2 className="text-xl md:text-2xl font-bold text-foreground">{trade.symbol}</h2>
            <span
              className={`text-sm px-3 py-1 rounded ${
                trade.type === 'long' ? 'bg-success/10 text-success' : 'bg-destructive/10 text-destructive'
              }`}
            >
              {trade.type.toUpperCase()}
            </span>
          </div>
          <Button variant="ghost" size="icon" iconName="X" onClick={onClose} />
        </div>

        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            {getStatusBadge(trade.status)}
            <Button
              variant="outline"
              size="sm"
              iconName="Edit"
              iconPosition="left"
              onClick={() => {
                onEdit(trade);
                onClose();
              }}
            >
              Edit Trade
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="bg-muted/50 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <Icon name="Calendar" size={18} className="text-primary" />
                <span className="text-sm font-medium text-muted-foreground">Entry Details</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Date:</span>
                  <span className="text-sm font-medium text-foreground">{formatDate(trade.entryDate)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Price:</span>
                  <span className="text-sm font-medium text-foreground">{formatCurrency(trade.entryPrice)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Quantity:</span>
                  <span className="text-sm font-medium text-foreground">{trade.quantity} shares</span>
                </div>
                <div className="flex justify-between pt-2 border-t border-border">
                  <span className="text-sm font-semibold text-foreground">Total Cost:</span>
                  <span className="text-sm font-semibold text-foreground">
                    {formatCurrency(trade.entryPrice * trade.quantity)}
                  </span>
                </div>
              </div>
            </div>

            <div className="bg-muted/50 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <Icon name="TrendingUp" size={18} className="text-primary" />
                <span className="text-sm font-medium text-muted-foreground">Exit Details</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Date:</span>
                  <span className="text-sm font-medium text-foreground">{formatDate(trade.exitDate)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Price:</span>
                  <span className="text-sm font-medium text-foreground">
                    {trade.exitPrice ? formatCurrency(trade.exitPrice) : '—'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Duration:</span>
                  <span className="text-sm font-medium text-foreground">{calculateDuration()}</span>
                </div>
                <div className="flex justify-between pt-2 border-t border-border">
                  <span className="text-sm font-semibold text-foreground">Total Value:</span>
                  <span className="text-sm font-semibold text-foreground">
                    {trade.exitPrice ? formatCurrency(trade.exitPrice * trade.quantity) : '—'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-primary/5 to-accent/5 rounded-lg p-6 mb-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Icon name="DollarSign" size={20} className="text-primary" />
                <span className="text-base font-semibold text-foreground">Performance Summary</span>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="text-sm text-muted-foreground block mb-1">Profit/Loss</span>
                <span className={`text-2xl md:text-3xl font-bold ${getProfitLossColor(trade.profitLoss)}`}>
                  {formatCurrency(trade.profitLoss)}
                </span>
              </div>
              {calculateReturnPercentage() !== null && (
                <div>
                  <span className="text-sm text-muted-foreground block mb-1">Return %</span>
                  <span
                    className={`text-2xl md:text-3xl font-bold ${getProfitLossColor(
                      parseFloat(calculateReturnPercentage())
                    )}`}
                  >
                    {calculateReturnPercentage()}%
                  </span>
                </div>
              )}
            </div>
          </div>

          {trade.tags && trade.tags.length > 0 && (
            <div className="mb-6">
              <div className="flex items-center gap-2 mb-3">
                <Icon name="Tag" size={18} className="text-primary" />
                <span className="text-sm font-medium text-foreground">Strategy Tags</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {trade.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-accent/10 text-accent rounded-full text-xs font-medium"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          {trade.notes && (
            <div>
              <div className="flex items-center gap-2 mb-3">
                <Icon name="FileText" size={18} className="text-primary" />
                <span className="text-sm font-medium text-foreground">Trade Notes</span>
              </div>
              <div className="bg-muted/50 rounded-lg p-4">
                <p className="text-sm text-foreground whitespace-pre-wrap">{trade.notes}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TradeDetailModal;
