import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const AccountCard = ({ account, onEdit, onDelete }) => {
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6 hover:shadow-md transition-smooth flex flex-col h-full">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start gap-3 flex-1 min-w-0">
          <div className="w-10 h-10 md:w-12 md:h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
            <Icon name="Wallet" size={20} className="text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-base md:text-lg font-semibold text-foreground mb-1 truncate">
              {account?.name}
            </h3>
            <p className="text-xs text-muted-foreground truncate">ID: {account?.id}</p>
          </div>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0 ml-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onEdit(account)}
            iconName="Edit2"
            iconSize={18}
            className="hover:bg-muted"
            title="Edit Account Name"
          />
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onDelete(account)}
            iconName="Trash2"
            iconSize={18}
            className="hover:bg-destructive/10 hover:text-destructive"
            title="Delete Account"
          />
        </div>
      </div>
      
      <div className="mt-auto pt-4 border-t border-border">
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <span>Created</span>
          <span>{formatDate(account?.created_at)}</span>
        </div>
        <div className="flex items-center justify-between text-xs text-muted-foreground mt-1">
          <span>Last Updated</span>
          <span>{formatDate(account?.updated_at)}</span>
        </div>
      </div>
    </div>
  );
};

export default AccountCard;