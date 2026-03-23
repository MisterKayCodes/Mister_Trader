import React from 'react';

import Button from '../../../components/ui/Button';

const TradeMobileCard = ({ trade, onEdit, onDelete, onView }) => {
  const getProfitLossColor = (value) => {
    if (value > 0) return 'text-success';
    if (value < 0) return 'text-destructive';
    return 'text-muted-foreground';
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      open: { bg: 'bg-warning/10', text: 'text-warning', label: 'Open' },
      closed: { bg: 'bg-success/10', text: 'text-success', label: 'Closed' },
      pending: { bg: 'bg-muted', text: 'text-muted-foreground', label: 'Pending' }
    };

    const config = statusConfig?.[status] || statusConfig?.pending;
    return (
      <span className={`px-3 py-1 rounded-full text-xs font-medium ${config?.bg} ${config?.text}`}>
        {config?.label}
      </span>
    );
  };

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

  return (
    <div 
      className="bg-card border border-border rounded-lg p-4 hover:shadow-md transition-smooth cursor-pointer"
      onClick={() => onView(trade)}
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-lg font-bold text-foreground">{trade?.symbol}</span>
          <span className={`text-xs px-2 py-0.5 rounded ${
            trade?.type === 'long' ? 'bg-success/10 text-success' : 'bg-destructive/10 text-destructive'
          }`}>
            {trade?.type?.toUpperCase()}
          </span>
        </div>
        {getStatusBadge(trade?.status)}
      </div>
      <div className="space-y-2 mb-4">
        <div className="flex justify-between items-center">
          <span className="text-sm text-muted-foreground">Date:</span>
          <span className="text-sm font-medium text-foreground">{formatDate(trade?.entryDate)}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-muted-foreground">Entry Price:</span>
          <span className="text-sm font-medium text-foreground">{formatCurrency(trade?.entryPrice)}</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-muted-foreground">Exit Price:</span>
          <span className="text-sm font-medium text-foreground">
            {trade?.exitPrice ? formatCurrency(trade?.exitPrice) : '—'}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-muted-foreground">Quantity:</span>
          <span className="text-sm font-medium text-foreground">{trade?.quantity}</span>
        </div>
        <div className="flex justify-between items-center pt-2 border-t border-border">
          <span className="text-sm font-semibold text-foreground">P&L:</span>
          <span className={`text-base font-bold ${getProfitLossColor(trade?.profitLoss)}`}>
            {formatCurrency(trade?.profitLoss)}
          </span>
        </div>
      </div>
      <div className="flex items-center gap-2 pt-3 border-t border-border" onClick={(e) => e?.stopPropagation()}>
        <Button
          variant="outline"
          size="sm"
          iconName="Edit"
          iconPosition="left"
          onClick={() => onEdit(trade)}
          fullWidth
        >
          Edit
        </Button>
        <Button
          variant="destructive"
          size="sm"
          iconName="Trash2"
          onClick={() => onDelete(trade)}
        />
      </div>
    </div>
  );
};

export default TradeMobileCard;