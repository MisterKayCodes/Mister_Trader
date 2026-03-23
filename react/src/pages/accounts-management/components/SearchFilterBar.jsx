import React from 'react';
import Icon from '../../../components/AppIcon';

const SearchFilterBar = ({ 
  searchQuery, 
  onSearchChange
}) => {
  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6 mb-6">
      <div className="relative max-w-2xl w-full">
        <Icon 
          name="Search" 
          size={20} 
          className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none" 
        />
        <input
          type="text"
          placeholder="Search accounts by name..."
          value={searchQuery}
          onChange={(e) => onSearchChange(e?.target?.value)}
          className="w-full pl-10 pr-4 py-2.5 bg-background border border-input rounded-lg text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
        />
      </div>
    </div>
  );
};

export default SearchFilterBar;