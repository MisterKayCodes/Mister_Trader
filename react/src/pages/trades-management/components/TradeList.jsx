import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import TradeFilters from './TradeFilters';
import TradeTable from './TradeTable';
import TradeMobileCard from './TradeMobileCard';
import BulkActionsBar from './BulkActionsBar';
import Pagination from './Pagination';

const TradeList = ({ trades = [], onFilterChange, onDelete }) => {
  const navigate = useNavigate();
  const [sortConfig, setSortConfig] = useState({ column: 'entryDate', direction: 'desc' });
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(25);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  React.useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleSort = (column) => {
    const direction = sortConfig?.column === column && sortConfig?.direction === 'asc' ? 'desc' : 'asc';
    setSortConfig({ column, direction });
  };

  const handleEdit = (trade) => {
    navigate(`/trades-management/edit/${trade?.id}`);
  };

  const handleView = (trade) => {
    navigate(`/trades-management/details/${trade?.id}`);
  };

  const handleExport = (format) => {
    console.log(`Exporting trades in ${format} format`);
  };

  const handleAnalyze = () => {
    console.log('Analyzing selected trades');
  };

  const paginatedTrades = trades?.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  const totalPages = Math.ceil(trades?.length / pageSize);

  return (
    <div className="space-y-6">
      <TradeFilters 
        onFilterChange={onFilterChange}
        resultsCount={trades?.length}
      />

      <BulkActionsBar
        selectedCount={0}
        onExport={handleExport}
        onAnalyze={handleAnalyze}
      />

      {isMobile ? (
        <div className="grid grid-cols-1 gap-4">
          {paginatedTrades?.map((trade) => (
            <TradeMobileCard
              key={trade?.id}
              trade={trade}
              onEdit={handleEdit}
              onDelete={onDelete}
              onView={handleView}
            />
          ))}
        </div>
      ) : (
        <TradeTable
          trades={paginatedTrades}
          onEdit={handleEdit}
          onDelete={onDelete}
          onView={handleView}
          onSort={handleSort}
          sortConfig={sortConfig}
        />
      )}

      {trades?.length > 0 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          pageSize={pageSize}
          onPageChange={setCurrentPage}
          onPageSizeChange={(size) => {
            setPageSize(size);
            setCurrentPage(1);
          }}
          totalItems={trades?.length}
        />
      )}

      {trades?.length === 0 && (
        <div className="text-center py-12 bg-card border border-border rounded-lg">
          <Icon name="TrendingUp" size={48} className="mx-auto text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold text-foreground mb-2">No trades found</h3>
          <p className="text-sm text-muted-foreground mb-6">Start by creating your first trade</p>
          <Button
            variant="default"
            iconName="Plus"
            iconPosition="left"
            onClick={() => navigate('/trades-management/create')}
          >
            Create Trade
          </Button>
        </div>
      )}
    </div>
  );
};

export default TradeList;