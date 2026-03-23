import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';
import Button from '../../../components/ui/Button';
import TradeMediaUploader from './TradeMediaUploader';

const TradeEdit = ({ onSuccess }) => {
  const navigate = useNavigate();
  const { id } = useParams();

  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(true);
  const [strategies, setStrategies] = useState([]);
  const [plans, setPlans] = useState([]);
  const [media, setMedia] = useState([]);
  const [formData, setFormData] = useState({
    symbol: '',
    side: 'BUY',
    quantity: '',
    entry_price: '',
    strategy_id: '',
    plan_id: '',
    pre_trade_emotion: '',
    risk_reward: '',
    notes: ''
  });
  const [errors, setErrors] = useState({});

  // Fetch trade and dropdown data on mount or when id changes
  useEffect(() => {
    fetchTrade();
    fetchStrategies();
    fetchPlans();
  }, [id]);

  const fetchTrade = async () => {
    try {
      const token = localStorage.getItem('trader_token');
      const response = await axios.get(
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/trades/${id}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      const trade = response.data;
      setFormData({
        symbol: trade.symbol || '',
        side: trade.side || 'BUY',
        quantity: trade.quantity || '',
        entry_price: trade.entry_price || '',
        strategy_id: trade.strategy_id || '',
        plan_id: trade.plan_id || '',
        pre_trade_emotion: trade.pre_trade_emotion || '',
        risk_reward: trade.risk_reward || '',
        notes: trade.notes || ''
      });
      setMedia(trade.media || []);
    } catch (error) {
      console.error('Failed to fetch trade:', error);
    } finally {
      setFetchLoading(false);
    }
  };

  const fetchStrategies = async () => {
    try {
      const token = localStorage.getItem('trader_token');
      const response = await axios.get(
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/strategies/`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setStrategies(response.data.map(s => ({ value: s.id, label: s.name })) || []);
    } catch (error) {
      console.error('Failed to fetch strategies:', error);
    }
  };

  const fetchPlans = async () => {
    try {
      const token = localStorage.getItem('trader_token');
      const response = await axios.get(
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/plans/today`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setPlans(response.data.map(p => ({ value: p.id, label: p.name })) || []);
    } catch (error) {
      console.error('Failed to fetch plans:', error);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    if (!formData.symbol.trim()) newErrors.symbol = 'Symbol is required';
    if (!formData.quantity || parseFloat(formData.quantity) <= 0) newErrors.quantity = 'Valid quantity required';
    if (!formData.entry_price || parseFloat(formData.entry_price) <= 0) newErrors.entry_price = 'Valid entry price required';
    if (!formData.strategy_id) newErrors.strategy_id = 'Strategy is required';
    if (!formData.plan_id) newErrors.plan_id = 'Plan is required';
    if (!formData.pre_trade_emotion.trim()) newErrors.pre_trade_emotion = 'Pre-trade emotion is required';
    if (!formData.risk_reward.trim()) newErrors.risk_reward = 'Risk/Reward is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      const token = localStorage.getItem('trader_token');

      await axios.put(
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/trades/${id}`,
        formData,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      // Upload any new media files
      const newMediaFiles = media.filter(m => m.file);
      if (newMediaFiles.length > 0) {
        await uploadMedia(id, newMediaFiles);
      }

      if (onSuccess) onSuccess();
      navigate('/trades-management');
    } catch (error) {
      console.error('Failed to update trade:', error);
      setErrors({ submit: error.response?.data?.message || 'Failed to update trade' });
    } finally {
      setLoading(false);
    }
  };

  const uploadMedia = async (tradeId, files) => {
    try {
      const token = localStorage.getItem('trader_token');
      const uploadData = new FormData();

      files.forEach(fileObj => {
        if (fileObj.file) uploadData.append('files', fileObj.file);
      });

      await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/api/v1/trades/${tradeId}/media`,
        uploadData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      );
    } catch (error) {
      console.error('Failed to upload media:', error);
    }
  };

  const sideOptions = [
    { value: 'BUY', label: 'BUY' },
    { value: 'SELL', label: 'SELL' }
  ];

  const emotionOptions = [
    { value: 'confident', label: 'Confident' },
    { value: 'neutral', label: 'Neutral' },
    { value: 'anxious', label: 'Anxious' },
    { value: 'fearful', label: 'Fearful' },
    { value: 'greedy', label: 'Greedy' }
  ];

  if (fetchLoading) {
    return (
      <div className="bg-card border border-border rounded-lg p-12 text-center">
        <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-sm text-muted-foreground">Loading trade...</p>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-foreground mb-2">Edit Trade</h2>
        <p className="text-sm text-muted-foreground">Update trade details and add more media</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Symbol"
            type="text"
            value={formData.symbol}
            onChange={e => handleChange('symbol', e.target.value.toUpperCase())}
            placeholder="e.g., BTCUSD, ETHUSD"
            error={errors.symbol}
            required
          />
          <Select
            label="Side"
            options={sideOptions}
            value={formData.side}
            onChange={value => handleChange('side', value)}
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Quantity"
            type="number"
            value={formData.quantity}
            onChange={e => handleChange('quantity', e.target.value)}
            placeholder="Number of units"
            error={errors.quantity}
            required
          />
          <Input
            label="Entry Price"
            type="number"
            step="0.01"
            value={formData.entry_price}
            onChange={e => handleChange('entry_price', e.target.value)}
            placeholder="0.00"
            error={errors.entry_price}
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Select
            label="Strategy"
            options={strategies}
            value={formData.strategy_id}
            onChange={value => handleChange('strategy_id', value)}
            placeholder="Select strategy"
            error={errors.strategy_id}
            searchable
            required
          />
          <Select
            label="Plan (Today)"
            options={plans}
            value={formData.plan_id}
            onChange={value => handleChange('plan_id', value)}
            placeholder="Select plan"
            error={errors.plan_id}
            searchable
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Select
            label="Pre-Trade Emotion"
            options={emotionOptions}
            value={formData.pre_trade_emotion}
            onChange={value => handleChange('pre_trade_emotion', value)}
            placeholder="How do you feel?"
            error={errors.pre_trade_emotion}
            required
          />
          <Input
            label="Risk Reward Ratio"
            type="text"
            value={formData.risk_reward}
            onChange={e => handleChange('risk_reward', e.target.value)}
            placeholder="e.g., 1:3"
            error={errors.risk_reward}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">Trade Notes</label>
          <textarea
            value={formData.notes}
            onChange={e => handleChange('notes', e.target.value)}
            placeholder="Add any additional notes about this trade..."
            rows={4}
            className="w-full px-4 py-3 bg-background border border-input rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-smooth resize-none"
          />
        </div>

        <TradeMediaUploader media={media} onChange={setMedia} />

        {errors.submit && (
          <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded-lg text-sm">
            {errors.submit}
          </div>
        )}

        <div className="flex flex-col-reverse sm:flex-row gap-3 pt-4 border-t border-border">
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate('/trades-management')}
            fullWidth
          >
            Cancel
          </Button>
          <Button
            type="submit"
            variant="default"
            loading={loading}
            fullWidth
          >
            Update Trade
          </Button>
        </div>
      </form>
    </div>
  );
};

export default TradeEdit;
