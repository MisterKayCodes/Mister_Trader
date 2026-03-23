import React, { useState } from 'react';
import api from '../../../auth/api';
import Modal from '../../../components/ui/Modal';
import Input from '../../../components/ui/Input';
import Button from '../../../components/ui/Button';

const CreatePlanModal = ({ isOpen, onClose, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    market_conditions: '',
    overall_bias: 'NEUTRAL',
  });

  const handleChange = (field, value) => {
      setFormData(prev => ({ ...prev, [field]: value }));
      if (error) setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.title.trim()) return setError("Plan title is required");

    setLoading(true);
    try {
      const response = await api.post('/plans/', formData);
      onSuccess(response.data);
      onClose();
      // Reset form
      setFormData({ title: '', market_conditions: '', overall_bias: 'NEUTRAL' });
    } catch (err) {
      console.error('Failed to create plan:', err);
      const detail = err.response?.data?.detail;
      const message = Array.isArray(detail) ? detail[0]?.msg : (detail || err.response?.data?.message || 'Failed to create plan');
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Create New Trade Plan">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
            <div className="bg-destructive/10 border border-destructive text-destructive px-3 py-2 rounded-lg text-sm">
              {error}
            </div>
        )}
        <Input
          label="Plan Title"
          type="text"
          value={formData.title}
          onChange={(e) => handleChange('title', e.target.value)}
          placeholder="e.g. Wednesday FOMC Strategy"
          required
        />
        <div>
          <label className="block text-sm font-medium text-foreground mb-2">Overall Bias</label>
          <select
            value={formData.overall_bias}
            onChange={(e) => handleChange('overall_bias', e.target.value)}
            className="w-full px-4 py-3 bg-background border border-input rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-smooth"
          >
            <option value="BULLISH">Bullish</option>
            <option value="BEARISH">Bearish</option>
            <option value="NEUTRAL">Neutral</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-foreground mb-2">Market Conditions</label>
          <textarea
            value={formData.market_conditions}
            onChange={(e) => handleChange('market_conditions', e.target.value)}
            placeholder="What is the current state of the market? (e.g. ranging, high volatility)"
            rows={2}
            className="w-full px-4 py-3 bg-background border border-input rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-smooth resize-none"
          />
        </div>
        <div className="flex gap-3 justify-end pt-4 mt-6 border-t border-border">
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" variant="primary" loading={loading}>
            Create Plan
          </Button>
        </div>
      </form>
    </Modal>
  );
};

export default CreatePlanModal;
