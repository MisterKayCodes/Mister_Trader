import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const BulkActionsBar = ({ selectedCount, onExport, onAnalyze }) => {
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async (format) => {
    setIsExporting(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    onExport(format);
    setIsExporting(false);
  };

  if (selectedCount === 0) {
    return (
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <Icon name="Database" size={20} className="text-muted-foreground" />
          <span className="text-sm text-muted-foreground">
            Select trades to perform bulk actions
          </span>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            iconName="Download"
            iconPosition="left"
            onClick={() => handleExport('csv')}
            loading={isExporting}
          >
            Export All
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-primary/10 border border-primary/20 rounded-lg p-4">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-primary flex items-center justify-center">
            <span className="text-sm font-bold text-primary-foreground">{selectedCount}</span>
          </div>
          <div>
            <span className="text-sm font-semibold text-foreground block">
              {selectedCount} {selectedCount === 1 ? 'trade' : 'trades'} selected
            </span>
            <span className="text-xs text-muted-foreground">Choose an action to perform</span>
          </div>
        </div>
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Button
            variant="outline"
            size="sm"
            iconName="BarChart3"
            iconPosition="left"
            onClick={onAnalyze}
            fullWidth
          >
            Analyze
          </Button>
          <Button
            variant="outline"
            size="sm"
            iconName="Download"
            iconPosition="left"
            onClick={() => handleExport('csv')}
            loading={isExporting}
          >
            Export
          </Button>
        </div>
      </div>
    </div>
  );
};

export default BulkActionsBar;