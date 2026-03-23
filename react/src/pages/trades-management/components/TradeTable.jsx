import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';

import TradeTableRow from './TradeTableRow';

const TradeTable = ({ trades, onEdit, onDelete, onView, onSort, sortConfig }) => {
  const [selectAll, setSelectAll] = useState(false);
  const [selectedTrades, setSelectedTrades] = useState([]);

  const handleSort = (column) => {
    onSort(column);
  };

  const getSortIcon = (column) => {
    if (sortConfig?.column !== column) {
      return <Icon name="ChevronsUpDown" size={16} className="text-muted-foreground" />;
    }
    return sortConfig?.direction === 'asc' 
      ? <Icon name="ChevronUp" size={16} className="text-primary" />
      : <Icon name="ChevronDown" size={16} className="text-primary" />;
  };

  const handleSelectAll = () => {
    if (selectAll) {
      setSelectedTrades([]);
    } else {
      setSelectedTrades(trades?.map(t => t?.id));
    }
    setSelectAll(!selectAll);
  };

  const columns = [
    { key: 'entryDate', label: 'Date', sortable: true },
    { key: 'symbol', label: 'Symbol', sortable: true },
    { key: 'entryPrice', label: 'Entry Price', sortable: true },
    { key: 'exitPrice', label: 'Exit Price', sortable: true },
    { key: 'quantity', label: 'Quantity', sortable: true },
    { key: 'profitLoss', label: 'P&L', sortable: true },
    { key: 'status', label: 'Status', sortable: true },
    { key: 'actions', label: 'Actions', sortable: false }
  ];

  if (trades?.length === 0) {
    return (
      <div className="bg-card border border-border rounded-lg p-8 md:p-12 text-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-16 h-16 md:w-20 md:h-20 rounded-full bg-muted flex items-center justify-center">
            <Icon name="TrendingUp" size={32} className="text-muted-foreground" />
          </div>
          <div>
            <h3 className="text-lg md:text-xl font-semibold text-foreground mb-2">No Trades Found</h3>
            <p className="text-sm md:text-base text-muted-foreground">
              Start tracking your trades by adding your first trade entry
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden">
      <div className="overflow-x-auto scrollbar-custom">
        <table className="w-full min-w-[800px]">
          <thead className="bg-muted/50 border-b border-border">
            <tr>
              {columns?.map((column) => (
                <th
                  key={column?.key}
                  className="px-4 py-3 text-left text-xs font-semibold text-muted-foreground uppercase tracking-wider"
                >
                  {column?.sortable ? (
                    <button
                      onClick={() => handleSort(column?.key)}
                      className="flex items-center gap-2 hover:text-foreground transition-smooth focus-ring rounded"
                    >
                      {column?.label}
                      {getSortIcon(column?.key)}
                    </button>
                  ) : (
                    column?.label
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {trades?.map((trade) => (
              <TradeTableRow
                key={trade?.id}
                trade={trade}
                onEdit={onEdit}
                onDelete={onDelete}
                onView={onView}
              />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TradeTable;