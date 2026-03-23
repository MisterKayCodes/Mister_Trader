import React, { useState } from 'react';
import api from '../../../auth/api';
import Modal from '../../../components/ui/Modal';
import Input from '../../../components/ui/Input';
import Button from '../../../components/ui/Button';

const CreateStrategyModal = ({ isOpen, onClose, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    rules: '',
    timeframe: '15m'
  });

  const handleChange = (field, value) => {
      setFormData(prev => ({ ...prev, [field]: value }));
      if (error) setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name.trim()) return setError("Strategy name is required");

    setLoading(true);
    try {
      const response = await api.post('/strategies/', formData);
      onSuccess(response.data);
      onClose();
      // Reset form
      setFormData({ name: '', description: '', rules: '', timeframe: '15m' });
    } catch (err) {
      console.error('Failed to create strategy:', err);
      const detail = err.response?.data?.detail;
      const message = Array.isArray(detail) ? detail[0]?.msg : (detail || err.response?.data?.message || 'Failed to create strategy');
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Create New Strategy">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
            <div className="bg-destructive/10 border border-destructive text-destructive px-3 py-2 rounded-lg text-sm">
              {error}
            </div>
        )}
        <Input
          label="Strategy Name"
          type="text"
          value={formData.name}
          onChange={(e) => handleChange('name', e.target.value)}
          placeholder="e.g. OrB Breakout"
          required
        />
        <Input
          label="Timeframe"
          type="text"
          value={formData.timeframe}
          onChange={(e) => handleChange('timeframe', e.target.value)}
          placeholder="e.g. 5m, 15m, 1H"
        />
        <div>
          <label className="block text-sm font-medium text-foreground mb-2">Description</label>
          <textarea
            value={formData.description}
            onChange={(e) => handleChange('description', e.target.value)}
            placeholder="What is the core idea of this strategy?"
            rows={2}
            className="w-full px-4 py-3 bg-background border border-input rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-smooth resize-none"
          />
        </div>
        <div className="flex gap-3 justify-end pt-4 mt-6 border-t border-border">
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" loading={loading}>
            Create Strategy
          </Button>
        </div>
      </form>
    </Modal>
  );
};

export default CreateStrategyModal;
