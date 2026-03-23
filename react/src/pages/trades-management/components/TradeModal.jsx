import React, { useState, useEffect } from 'react';

import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';
import Button from '../../../components/ui/Button';

const TradeModal = ({ isOpen, onClose, trade, onSave, mode = 'create' }) => {
  const [formData, setFormData] = useState({
    symbol: '',
    type: 'long',
    entryDate: '',
    entryPrice: '',
    exitDate: '',
    exitPrice: '',
    quantity: '',
    status: 'open',
    notes: '',
    tags: []
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (trade && mode === 'edit') {
      setFormData({
        symbol: trade?.symbol || '',
        type: trade?.type || 'long',
        entryDate: trade?.entryDate || '',
        entryPrice: trade?.entryPrice || '',
        exitDate: trade?.exitDate || '',
        exitPrice: trade?.exitPrice || '',
        quantity: trade?.quantity || '',
        status: trade?.status || 'open',
        notes: trade?.notes || '',
        tags: trade?.tags || []
      });
    } else {
      setFormData({
        symbol: '',
        type: 'long',
        entryDate: new Date()?.toISOString()?.split('T')?.[0],
        entryPrice: '',
        exitDate: '',
        exitPrice: '',
        quantity: '',
        status: 'open',
        notes: '',
        tags: []
      });
    }
    setErrors({});
  }, [trade, mode, isOpen]);

  const tradeTypeOptions = [
    { value: 'long', label: 'Long Position' },
    { value: 'short', label: 'Short Position' }
  ];

  const statusOptions = [
    { value: 'open', label: 'Open' },
    { value: 'closed', label: 'Closed' },
    { value: 'pending', label: 'Pending' }
  ];

  const tagOptions = [
    { value: 'breakout', label: 'Breakout Strategy' },
    { value: 'reversal', label: 'Reversal Pattern' },
    { value: 'trend', label: 'Trend Following' },
    { value: 'momentum', label: 'Momentum Play' },
    { value: 'earnings', label: 'Earnings Trade' },
    { value: 'news', label: 'News-Based' }
  ];

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors?.[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData?.symbol?.trim()) {
      newErrors.symbol = 'Symbol is required';
    }
    if (!formData?.entryDate) {
      newErrors.entryDate = 'Entry date is required';
    }
    if (!formData?.entryPrice || parseFloat(formData?.entryPrice) <= 0) {
      newErrors.entryPrice = 'Valid entry price is required';
    }
    if (!formData?.quantity || parseInt(formData?.quantity) <= 0) {
      newErrors.quantity = 'Valid quantity is required';
    }
    if (formData?.status === 'closed' && !formData?.exitPrice) {
      newErrors.exitPrice = 'Exit price required for closed trades';
    }
    if (formData?.status === 'closed' && !formData?.exitDate) {
      newErrors.exitDate = 'Exit date required for closed trades';
    }

    setErrors(newErrors);
    return Object.keys(newErrors)?.length === 0;
  };

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (validateForm()) {
      const profitLoss = formData?.exitPrice 
        ? (formData?.type === 'long' 
            ? (parseFloat(formData?.exitPrice) - parseFloat(formData?.entryPrice)) * parseInt(formData?.quantity)
            : (parseFloat(formData?.entryPrice) - parseFloat(formData?.exitPrice)) * parseInt(formData?.quantity))
        : 0;

      onSave({
        ...trade,
        ...formData,
        profitLoss,
        symbol: formData?.symbol?.toUpperCase()
      });
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm">
      <div className="bg-card border border-border rounded-lg w-full max-w-2xl max-h-[90vh] overflow-y-auto scrollbar-custom">
        <div className="sticky top-0 bg-card border-b border-border px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl md:text-2xl font-semibold text-foreground">
            {mode === 'edit' ? 'Edit Trade' : 'Add New Trade'}
          </h2>
          <Button
            variant="ghost"
            size="icon"
            iconName="X"
            onClick={onClose}
          />
        </div>

        <form onSubmit={handleSubmit} className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <Input
              label="Symbol"
              type="text"
              value={formData?.symbol}
              onChange={(e) => handleChange('symbol', e?.target?.value?.toUpperCase())}
              placeholder="e.g., AAPL, TSLA"
              error={errors?.symbol}
              required
            />
            <Select
              label="Trade Type"
              options={tradeTypeOptions}
              value={formData?.type}
              onChange={(value) => handleChange('type', value)}
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <Input
              label="Entry Date"
              type="date"
              value={formData?.entryDate}
              onChange={(e) => handleChange('entryDate', e?.target?.value)}
              error={errors?.entryDate}
              required
            />
            <Input
              label="Entry Price"
              type="number"
              value={formData?.entryPrice}
              onChange={(e) => handleChange('entryPrice', e?.target?.value)}
              placeholder="0.00"
              error={errors?.entryPrice}
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <Input
              label="Exit Date"
              type="date"
              value={formData?.exitDate}
              onChange={(e) => handleChange('exitDate', e?.target?.value)}
              error={errors?.exitDate}
            />
            <Input
              label="Exit Price"
              type="number"
              value={formData?.exitPrice}
              onChange={(e) => handleChange('exitPrice', e?.target?.value)}
              placeholder="0.00"
              error={errors?.exitPrice}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <Input
              label="Quantity"
              type="number"
              value={formData?.quantity}
              onChange={(e) => handleChange('quantity', e?.target?.value)}
              placeholder="Number of shares"
              error={errors?.quantity}
              required
            />
            <Select
              label="Status"
              options={statusOptions}
              value={formData?.status}
              onChange={(value) => handleChange('status', value)}
              required
            />
          </div>

          <div className="mb-6">
            <Select
              label="Strategy Tags"
              options={tagOptions}
              value={formData?.tags}
              onChange={(value) => handleChange('tags', value)}
              multiple
              searchable
              clearable
              description="Select applicable trading strategies"
            />
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-foreground mb-2">
              Trade Notes
            </label>
            <textarea
              value={formData?.notes}
              onChange={(e) => handleChange('notes', e?.target?.value)}
              placeholder="Add any additional notes about this trade..."
              rows={4}
              className="w-full px-4 py-3 bg-background border border-input rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-smooth resize-none"
            />
          </div>

          <div className="flex flex-col-reverse sm:flex-row gap-3 pt-4 border-t border-border">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              fullWidth
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="default"
              iconName="Save"
              iconPosition="left"
              fullWidth
            >
              {mode === 'edit' ? 'Update Trade' : 'Add Trade'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TradeModal;