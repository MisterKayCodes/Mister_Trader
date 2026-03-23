import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';
import Button from '../../../components/ui/Button';

const TradeFilters = ({ onFilterChange, resultsCount }) => {
  const [filters, setFilters] = useState({
    dateFrom: '',
    dateTo: '',
    symbol: '',
    tradeType: '',
    profitLossMin: '',
    profitLossMax: '',
    duration: '',
    tags: []
  });

  const [showAdvanced, setShowAdvanced] = useState(false);

  const tradeTypeOptions = [
    { value: '', label: 'All Trade Types' },
    { value: 'long', label: 'Long Position' },
    { value: 'short', label: 'Short Position' },
    { value: 'day', label: 'Day Trade' },
    { value: 'swing', label: 'Swing Trade' },
    { value: 'scalp', label: 'Scalp Trade' }
  ];

  const durationOptions = [
    { value: '', label: 'Any Duration' },
    { value: 'intraday', label: 'Intraday (Same Day)' },
    { value: '1-3', label: '1-3 Days' },
    { value: '4-7', label: '4-7 Days' },
    { value: '8-30', label: '1-4 Weeks' },
    { value: '30+', label: 'Over 1 Month' }
  ];

  const tagOptions = [
    { value: 'breakout', label: 'Breakout Strategy' },
    { value: 'reversal', label: 'Reversal Pattern' },
    { value: 'trend', label: 'Trend Following' },
    { value: 'momentum', label: 'Momentum Play' },
    { value: 'earnings', label: 'Earnings Trade' },
    { value: 'news', label: 'News-Based' }
  ];

  const handleFilterChange = (field, value) => {
    const updatedFilters = { ...filters, [field]: value };
    setFilters(updatedFilters);
    onFilterChange(updatedFilters);
  };

  const handleReset = () => {
    const resetFilters = {
      dateFrom: '',
      dateTo: '',
      symbol: '',
      tradeType: '',
      profitLossMin: '',
      profitLossMax: '',
      duration: '',
      tags: []
    };
    setFilters(resetFilters);
    onFilterChange(resetFilters);
    setShowAdvanced(false);
  };

  const hasActiveFilters = Object.values(filters).some(value =>
    Array.isArray(value) ? value.length > 0 : value !== ''
  );

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6 mb-4 md:mb-6">
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-4">
        <div className="flex items-center gap-3">
          <Icon name="Filter" size={20} className="text-primary" />
          <h2 className="text-lg md:text-xl font-semibold text-foreground">Filter Trades</h2>
          {typeof resultsCount === 'number' && (
            <span className="px-3 py-1 bg-accent/10 text-accent rounded-full text-sm font-medium">
              {resultsCount} {resultsCount === 1 ? 'trade' : 'trades'}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            iconName="RotateCcw"
            iconPosition="left"
            onClick={handleReset}
            disabled={!hasActiveFilters}
          >
            Reset Filters
          </Button>
          <Button
            variant="outline"
            size="sm"
            iconName={showAdvanced ? "ChevronUp" : "ChevronDown"}
            iconPosition="right"
            onClick={() => setShowAdvanced(!showAdvanced)}
          >
            Advanced
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Input
          type="date"
          label="From Date"
          value={filters.dateFrom}
          onChange={e => handleFilterChange('dateFrom', e.target.value)}
          placeholder="Start date"
        />
        <Input
          type="date"
          label="To Date"
          value={filters.dateTo}
          onChange={e => handleFilterChange('dateTo', e.target.value)}
          placeholder="End date"
        />
        <Input
          type="search"
          label="Symbol"
          value={filters.symbol}
          onChange={e => handleFilterChange('symbol', e.target.value.toUpperCase())}
          placeholder="e.g., BTCUSD, ETHUSD, EURUSD"
        />
        <Select
          label="Trade Type"
          options={tradeTypeOptions}
          value={filters.tradeType}
          onChange={value => handleFilterChange('tradeType', value)}
        />
      </div>

      {showAdvanced && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-4 pt-4 border-t border-border">
          <Input
            type="number"
            label="Min P&L ($)"
            value={filters.profitLossMin}
            onChange={e => handleFilterChange('profitLossMin', e.target.value)}
            placeholder="Minimum profit/loss"
          />
          <Input
            type="number"
            label="Max P&L ($)"
            value={filters.profitLossMax}
            onChange={e => handleFilterChange('profitLossMax', e.target.value)}
            placeholder="Maximum profit/loss"
          />
          <Select
            label="Trade Duration"
            options={durationOptions}
            value={filters.duration}
            onChange={value => handleFilterChange('duration', value)}
          />
          <Select
            label="Strategy Tags"
            options={tagOptions}
            value={filters.tags}
            onChange={value => handleFilterChange('tags', value)}
            multiple
            searchable
            clearable
          />
        </div>
      )}
    </div>
  );
};

export default TradeFilters;
