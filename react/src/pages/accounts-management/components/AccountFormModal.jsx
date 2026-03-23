import React, { useState, useEffect } from 'react';

import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';

const AccountFormModal = ({ isOpen, onClose, onSubmit, account, mode }) => {
  const [formData, setFormData] = useState({
    name: ''
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (account && mode === 'edit') {
      setFormData({
        name: account?.name || ''
      });
    } else {
      setFormData({
        name: ''
      });
    }
    setErrors({});
  }, [account, mode, isOpen]);


  const validateForm = () => {
    const newErrors = {};

    if (!formData?.name?.trim()) {
      newErrors.name = 'Account name is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e?.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    const submitData = {
      ...formData
    };

    if (mode === 'edit' && account) {
      submitData.id = account?.id;
    }

    try {
      await onSubmit(submitData);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors?.[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm">
      <div className="bg-card border border-border rounded-lg shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-card border-b border-border px-4 md:px-6 py-4 flex items-center justify-between">
          <h2 className="text-lg md:text-xl font-semibold text-foreground">
            {mode === 'edit' ? 'Edit Account' : 'Add New Account'}
          </h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            iconName="X"
            iconSize={20}
            disabled={isSubmitting}
          />
        </div>

        <form onSubmit={handleSubmit} className="p-4 md:p-6 space-y-4 md:space-y-6">
          <Input
            label="Account Name"
            type="text"
            placeholder="e.g., Main Trading Account or Vault A"
            value={formData?.name}
            onChange={(e) => handleChange('name', e?.target?.value)}
            error={errors?.name}
            required
            disabled={isSubmitting}
          />

          <div className="flex flex-col-reverse sm:flex-row gap-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              disabled={isSubmitting}
              fullWidth
              className="sm:flex-1"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="default"
              loading={isSubmitting}
              fullWidth
              className="sm:flex-1"
            >
              {mode === 'edit' ? 'Update Account' : 'Create Account'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AccountFormModal;