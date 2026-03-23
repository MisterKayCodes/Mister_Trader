import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../../auth/api';
import Input from '../../../components/ui/Input';
import Select from '../../../components/ui/Select';
import Button from '../../../components/ui/Button';
import TradeMediaUploader from './TradeMediaUploader';
import CreateStrategyModal from './CreateStrategyModal';
import CreatePlanModal from './CreatePlanModal';

const TradeCreateForm = ({ onSuccess }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [strategies, setStrategies] = useState([]);
  const [plans, setPlans] = useState([]);
  const [isStrategyModalOpen, setStrategyModalOpen] = useState(false);
  const [isPlanModalOpen, setPlanModalOpen] = useState(false);
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
    notes: '',
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      await Promise.all([fetchStrategies(), fetchPlans()]);
    };
    fetchData();
  }, []);

  const fetchStrategies = async () => {
    try {
      const response = await api.get('/strategies/');
      const options = response.data?.map((s) => ({ value: s.id, label: s.name })) || [];
      setStrategies(options);
    } catch (error) {
      console.error('Failed to fetch strategies:', error);
    }
  };

  const fetchPlans = async () => {
    try {
      const response = await api.get('/plans/today');
      const plan = response.data;
      const options = plan ? [{ value: plan.id, label: plan.title }] : [];
      setPlans(options);
    } catch (error) {
      if (error.response?.status !== 404) {
        console.error('Failed to fetch plan:', error);
      }
      setPlans([]);
    }
  };

  const handleStrategyCreated = async (newStrategy) => {
     await fetchStrategies();
     setFormData(prev => ({ ...prev, strategy_id: newStrategy.id }));
  };

  const handlePlanCreated = async (newPlan) => {
     await fetchPlans();
     setFormData(prev => ({ ...prev, plan_id: newPlan.id }));
  };

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors((prev) => ({ ...prev, [field]: '' }));
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
      const accountId = localStorage.getItem('selected_account_id');
      if (!accountId) {
         setErrors({ submit: "No Trading Account selected! Please select an account at the top right before creating a trade." });
         setLoading(false);
         return;
      }

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
         account_id: parseInt(accountId),
         risk_reward_ratio: parsedRR,
         entry_price: formData.entry_price ? parseFloat(formData.entry_price) : null,
         strategy_id: formData.strategy_id ? parseInt(formData.strategy_id) : null,
         plan_id: formData.plan_id ? parseInt(formData.plan_id) : null,
         quantity: parseFloat(formData.quantity)
      };

      // Clean up frontend variables the backend hates
      delete payload.risk_reward;

      const response = await api.post('/trades', payload);

      const tradeId = response.data?.id;
      if (tradeId && media.length > 0) {
        await uploadMedia(tradeId);
      }

      onSuccess?.();
      navigate('/trades-management');
    } catch (error) {
      console.error('Failed to create trade:', error);
      const detail = error.response?.data?.detail;
      let errMsg = 'Failed to create trade';
      if (Array.isArray(detail)) {
         errMsg = detail.map(e => `${e.loc?.join('.')}: ${e.msg}`).join(', ');
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

  const uploadMedia = async (tradeId) => {
    try {
      const formPayload = new FormData();
      media.forEach((item) => {
        if (item.file) {
          formPayload.append('files', item.file);
        }
      });

      await api.post(`/trades/${tradeId}/media`, formPayload, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    } catch (error) {
      console.error('Failed to upload media:', error);
    }
  };

  const sideOptions = [
    { value: 'BUY', label: 'BUY' },
    { value: 'SELL', label: 'SELL' },
  ];

  const emotionOptions = [
    { value: 'confident', label: 'Confident' },
    { value: 'neutral', label: 'Neutral' },
    { value: 'anxious', label: 'Anxious' },
    { value: 'fearful', label: 'Fearful' },
    { value: 'greedy', label: 'Greedy' },
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-foreground mb-2">Create New Trade</h2>
        <p className="text-sm text-muted-foreground">Fill in the trade details and attach any relevant media</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Symbol"
            type="text"
            value={formData.symbol}
            onChange={(e) => handleChange('symbol', e.target.value.toUpperCase())}
            placeholder="e.g., BTCUSD, EURUSD, ETHBTC"
            error={errors.symbol}
            required
          />
          <Select
            label="Side"
            options={sideOptions}
            value={formData.side}
            onChange={handleChange.bind(null, 'side')}
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Quantity"
            type="number"
            value={formData.quantity}
            onChange={(e) => handleChange('quantity', e.target.value)}
            placeholder="Number of units"
            error={errors.quantity}
            required
          />
          <Input
            label="Entry Price"
            type="number"
            step="0.0001"
            value={formData.entry_price}
            onChange={(e) => handleChange('entry_price', e.target.value)}
            placeholder="0.0000"
            error={errors.entry_price}
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Select
            label="Strategy"
            actionLabel="+ Add New"
            onAction={() => setStrategyModalOpen(true)}
            options={strategies}
            value={formData.strategy_id}
            onChange={handleChange.bind(null, 'strategy_id')}
            placeholder="Select strategy"
            error={errors.strategy_id}
            searchable
            required
          />
          <Select
            label="Plan (Today)"
            actionLabel="+ Add New"
            onAction={() => setPlanModalOpen(true)}
            options={plans}
            value={formData.plan_id}
            onChange={handleChange.bind(null, 'plan_id')}
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
            onChange={handleChange.bind(null, 'pre_trade_emotion')}
            placeholder="How do you feel?"
            error={errors.pre_trade_emotion}
            required
          />
          <Input
            label="Risk Reward Ratio"
            type="text"
            value={formData.risk_reward}
            onChange={(e) => handleChange('risk_reward', e.target.value)}
            placeholder="e.g., 1:3"
            error={errors.risk_reward}
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">Trade Notes</label>
          <textarea
            value={formData.notes}
            onChange={(e) => handleChange('notes', e.target.value)}
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
          <Button type="submit" variant="default" loading={loading} fullWidth>
            Create Trade
          </Button>
        </div>
      </form>

      <CreateStrategyModal
         isOpen={isStrategyModalOpen}
         onClose={() => setStrategyModalOpen(false)}
         onSuccess={handleStrategyCreated}
      />
      <CreatePlanModal
         isOpen={isPlanModalOpen}
         onClose={() => setPlanModalOpen(false)}
         onSuccess={handlePlanCreated}
      />
    </div>
  );
};

export default TradeCreateForm;
