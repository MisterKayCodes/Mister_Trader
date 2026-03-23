import React from 'react';

import Button from '../../../components/ui/Button';

const TradeTableRow = ({ trade, onEdit, onDelete, onView }) => {
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
    if (value === null || value === undefined) return '—';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    })?.format(value);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '—';
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'Invalid Date';
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <tr 
      className="border-b border-border hover:bg-muted/50 transition-smooth cursor-pointer"
      onClick={() => onView(trade)}
    >
      <td className="px-4 py-4 text-sm text-foreground font-medium whitespace-nowrap">
        {formatDate(trade?.open_timestamp || trade?.created_at)}
      </td>
      <td className="px-4 py-4">
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold text-foreground">{trade?.symbol}</span>
          <span className={`text-xs px-2 py-0.5 rounded ${
            trade?.side?.toUpperCase() === 'BUY' || trade?.side?.toUpperCase() === 'LONG' 
              ? 'bg-success/10 text-success' 
              : 'bg-destructive/10 text-destructive'
          }`}>
            {trade?.side?.toUpperCase()}
          </span>
        </div>
      </td>
      <td className="px-4 py-4 text-sm text-foreground whitespace-nowrap">
        {formatCurrency(trade?.entry_price)}
      </td>
      <td className="px-4 py-4 text-sm text-foreground whitespace-nowrap">
        {trade?.exit_price ? formatCurrency(trade?.exit_price) : '—'}
      </td>
      <td className="px-4 py-4 text-sm text-foreground whitespace-nowrap">
        {trade?.quantity}
      </td>
      <td className="px-4 py-4 whitespace-nowrap">
        <span className={`text-sm font-semibold ${getProfitLossColor(trade?.pnl)}`}>
          {trade?.pnl ? formatCurrency(trade?.pnl) : '—'}
        </span>
      </td>
      <td className="px-4 py-4">
        {getStatusBadge(trade?.state || 'pending')}
      </td>
      <td className="px-4 py-4">
        <div className="flex items-center gap-2" onClick={(e) => e?.stopPropagation()}>
          <Button
            variant="ghost"
            size="icon"
            iconName="Edit"
            onClick={() => onEdit(trade)}
            className="hover:bg-primary/10 hover:text-primary"
          />
          <Button
            variant="ghost"
            size="icon"
            iconName="Trash2"
            onClick={() => onDelete(trade)}
            className="hover:bg-destructive/10 hover:text-destructive"
          />
        </div>
      </td>
    </tr>
  );
};

export default TradeTableRow;