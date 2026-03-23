import React from 'react';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';
import Button from '../../../components/ui/Button';

const SearchFilterPanel = ({ 
  searchQuery, 
  onSearchChange, 
  dateRange, 
  onDateRangeChange,
  emotionFilter,
  onEmotionFilterChange,
  onClearFilters 
}) => {
  const dateRangeOptions = [
    { value: 'all', label: 'All Time' },
    { value: 'today', label: 'Today' },
    { value: 'week', label: 'This Week' },
    { value: 'month', label: 'This Month' },
    { value: 'quarter', label: 'This Quarter' },
    { value: 'year', label: 'This Year' }
  ];

  const emotionFilterOptions = [
    { value: 'all', label: 'All Emotions' },
    { value: 'fear', label: 'Fear' },
    { value: 'greed', label: 'Greed' },
    { value: 'confidence', label: 'Confidence' },
    { value: 'uncertainty', label: 'Uncertainty' },
    { value: 'excitement', label: 'Excitement' },
    { value: 'frustration', label: 'Frustration' },
    { value: 'calm', label: 'Calm' },
    { value: 'anxiety', label: 'Anxiety' }
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-base md:text-lg font-semibold text-foreground">Search & Filter</h3>
        <Button
          variant="ghost"
          size="sm"
          onClick={onClearFilters}
          iconName="X"
          iconPosition="left"
        >
          Clear
        </Button>
      </div>
      <div className="space-y-4">
        <Input
          type="search"
          placeholder="Search psychology entries..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e?.target?.value)}
          className="w-full"
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Select
            label="Date Range"
            options={dateRangeOptions}
            value={dateRange}
            onChange={onDateRangeChange}
            placeholder="Select date range"
          />

          <Select
            label="Emotion Filter"
            options={emotionFilterOptions}
            value={emotionFilter}
            onChange={onEmotionFilterChange}
            placeholder="Filter by emotion"
          />
        </div>
      </div>
    </div>
  );
};

export default SearchFilterPanel;