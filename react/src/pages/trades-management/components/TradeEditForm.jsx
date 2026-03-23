import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../../auth/api';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';
import Button from '../../../components/ui/Button';
import TradeMediaUploader from './TradeMediaUploader';

const TradeEditForm = ({ onSuccess }) => {
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
    exit_price: '',
    pnl: '',
    state: 'pending',
    outcome: '',
    strategy_id: '',
    plan_id: '',
    pre_trade_emotion: '',
    post_trade_emotion: '',
    risk_reward: '',
    notes: ''
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    fetchTrade();
    fetchStrategies();
    fetchPlans();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const fetchTrade = async () => {
    try {
      const response = await api.get(`/trades/${id}`);
      const trade = response.data;

      setFormData({
        symbol: trade.symbol || '',
        side: trade.side || 'BUY',
        quantity: trade.quantity || '',
        entry_price: trade.entry_price || '',
        exit_price: trade.exit_price || '',
        pnl: trade.pnl || '',
        state: trade.state || 'pending',
        outcome: trade.outcome || '',
        strategy_id: trade.strategy_id || '',
        plan_id: trade.plan_id || '',
        pre_trade_emotion: trade.pre_trade_emotion || '',
        post_trade_emotion: trade.post_trade_emotion || '',
        risk_reward: trade.risk_reward_ratio ? `1:${trade.risk_reward_ratio}` : '',
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
      const response = await api.get('/strategies/');
      setStrategies(response.data.map(s => ({ value: s.id, label: s.name })) || []);
    } catch (error) {
      console.error('Failed to fetch strategies:', error);
    }
  };

  const fetchPlans = async () => {
    try {
      const response = await api.get('/plans/');
      setPlans(response.data.map(p => ({ value: p.id, label: p.title })) || []);
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
      let parsedRR = null;
      if (formData.risk_reward) {
         if (formData.risk_reward.includes(':')) {
             const parts = formData.risk_reward.split(':');
             if (parts.length === 2 && !isNaN(parseFloat(parts[1]))) {
                 parsedRR = parseFloat(parts[1]) / (parseFloat(parts[0]) || 1);
             }
         } else if (!isNaN(parseFloat(formData.risk_reward))) {
             parsedRR = parseFloat(formData.risk_reward);
         }
      }

      const payload = {
         ...formData,
         risk_reward_ratio: parsedRR,
         entry_price: formData.entry_price ? parseFloat(formData.entry_price) : null,
         exit_price: formData.exit_price ? parseFloat(formData.exit_price) : null,
         pnl: formData.pnl ? parseFloat(formData.pnl) : null,
         strategy_id: formData.strategy_id ? parseInt(formData.strategy_id) : null,
         plan_id: formData.plan_id ? parseInt(formData.plan_id) : null,
         quantity: parseFloat(formData.quantity)
      };

      delete payload.risk_reward;

      await api.put(`/trades/${id}`, payload);

      const newMediaFiles = media.filter(m => m.file);
      if (newMediaFiles.length > 0) {
        await uploadMedia(id, newMediaFiles);
      }

      if (onSuccess) onSuccess();
      navigate('/trades-management');
    } catch (error) {
      console.error('Failed to update trade:', error);
      const detail = error.response?.data?.detail;
      let errMsg = 'Failed to update trade';
      if (Array.isArray(detail)) {
         errMsg = detail.map(err => `${err.loc?.join('.')}: ${err.msg}`).join(', ');
      } else if (typeof detail === 'string') {
         errMsg = detail;
      } else if (error.response?.data?.message) {
         errMsg = error.response.data.message;
      }
      setErrors({ submit: errMsg });
    } finally {
      setLoading(false);
    }
  };

  const uploadMedia = async (tradeId, files) => {
    try {
      const uploadFormData = new FormData();

      files.forEach(fileObj => {
        if (fileObj.file) uploadFormData.append('files', fileObj.file);
      });

      await api.post(`/trades/${tradeId}/media`, uploadFormData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
      });
    } catch (error) {
      console.error('Failed to upload media:', error);
    }
  };

  const sideOptions = [
    { value: 'BUY', label: 'BUY' },
    { value: 'SELL', label: 'SELL' }
  ];

  const stateOptions = [
    { value: 'pending', label: 'Pending' },
    { value: 'active', label: 'Active' },
    { value: 'closed', label: 'Closed' }
  ];

  const outcomeOptions = [
    { value: '', label: 'None' },
    { value: 'WIN', label: 'Win' },
    { value: 'LOSS', label: 'Loss' },
    { value: 'BREAK_EVEN', label: 'Break Even' }
  ];

  const emotionOptions = [
    { value: '', label: 'None' },
    { value: 'confident', label: 'Confident' },
    { value: 'neutral', label: 'Neutral' },
    { value: 'anxious', label: 'Anxious' },
    { value: 'fearful', label: 'Fearful' },
    { value: 'greedy', label: 'Greedy' },
    { value: 'euphoric', label: 'Euphoric' },
    { value: 'frustrated', label: 'Frustrated' }
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
            label="State / Status"
            options={stateOptions}
            value={formData.state}
            onChange={value => handleChange('state', value)}
            required
          />
          <Input
            label="Exit Price"
            type="number"
            step="0.01"
            value={formData.exit_price}
            onChange={e => handleChange('exit_price', e.target.value)}
            placeholder="0.00"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="PnL (Profit & Loss)"
            type="number"
            step="0.01"
            value={formData.pnl}
            onChange={e => handleChange('pnl', e.target.value)}
            placeholder="0.00"
          />
          <Select
            label="Trade Outcome"
            options={outcomeOptions}
            value={formData.outcome}
            onChange={value => handleChange('outcome', value)}
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

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Select
            label="Pre-Trade Emotion"
            options={emotionOptions}
            value={formData.pre_trade_emotion}
            onChange={value => handleChange('pre_trade_emotion', value)}
            placeholder="How do you feel?"
            error={errors.pre_trade_emotion}
            required
          />
          <Select
            label="Post-Trade Emotion"
            options={emotionOptions}
            value={formData.post_trade_emotion}
            onChange={value => handleChange('post_trade_emotion', value)}
            placeholder="How did you feel?"
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

export default TradeEditForm;
