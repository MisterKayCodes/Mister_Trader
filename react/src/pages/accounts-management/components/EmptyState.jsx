import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const EmptyState = ({ onAddAccount, hasFilters }) => {
  return (
    <div className="bg-card border border-border rounded-lg p-8 md:p-12 text-center">
      <div className="w-16 h-16 md:w-20 md:h-20 rounded-full bg-muted flex items-center justify-center mx-auto mb-4 md:mb-6">
        <Icon name="Wallet" size={32} className="text-muted-foreground" />
      </div>
      
      <h3 className="text-lg md:text-xl font-semibold text-foreground mb-2">
        {hasFilters ? 'No Accounts Found' : 'No Trading Accounts Yet'}
      </h3>
      
      <p className="text-sm md:text-base text-muted-foreground mb-6 md:mb-8 max-w-md mx-auto">
        {hasFilters 
          ? 'No accounts match your current filters. Try adjusting your search criteria or clear filters to see all accounts.' :'Get started by adding your first trading account. Track your trades, monitor performance, and analyze your trading psychology across multiple accounts.'}
      </p>
      
      {!hasFilters && (
        <Button
          variant="default"
          onClick={onAddAccount}
          iconName="Plus"
          iconPosition="left"
        >
          Add Your First Account
        </Button>
      )}
    </div>
  );
};

export default EmptyState;