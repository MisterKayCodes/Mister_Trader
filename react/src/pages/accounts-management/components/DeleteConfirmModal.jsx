import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const DeleteConfirmModal = ({ isOpen, onClose, onConfirm, account, isDeleting }) => {
  if (!isOpen || !account) return null;

  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm">
      <div className="bg-card border border-border rounded-lg shadow-xl w-full max-w-md">
        <div className="p-4 md:p-6">
          <div className="flex items-start gap-4 mb-4">
            <div className="w-12 h-12 rounded-full bg-destructive/10 flex items-center justify-center flex-shrink-0">
              <Icon name="AlertTriangle" size={24} className="text-destructive" />
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-semibold text-foreground mb-2">
                Delete Account
              </h3>
              <p className="text-sm text-muted-foreground">
                Are you sure you want to delete <span className="font-medium text-foreground">"{account?.name}"</span>? This action cannot be undone and will permanently remove all associated data.
              </p>
            </div>
          </div>

          <div className="bg-muted rounded-lg p-4 mb-6">
            <div className="flex items-center gap-2 mb-2">
              <Icon name="Info" size={16} className="text-muted-foreground" />
              <span className="text-sm font-medium text-foreground">Account Details</span>
            </div>
            <div className="space-y-1 text-sm text-muted-foreground">
              <p>Broker: {account?.broker}</p>
              <p>Type: {account?.type}</p>
              <p>Balance: ${account?.balance?.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</p>
            </div>
          </div>

          <div className="flex flex-col-reverse sm:flex-row gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              disabled={isDeleting}
              fullWidth
              className="sm:flex-1"
            >
              Cancel
            </Button>
            <Button
              type="button"
              variant="destructive"
              onClick={onConfirm}
              loading={isDeleting}
              fullWidth
              className="sm:flex-1"
            >
              Delete Account
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmModal;