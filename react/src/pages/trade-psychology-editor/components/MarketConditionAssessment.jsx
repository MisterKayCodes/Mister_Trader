import React from 'react';
import Select from '../../../components/ui/Select';

const MarketConditionAssessment = ({ marketCondition, onConditionChange, volatility, onVolatilityChange }) => {
  const marketConditionOptions = [
    { value: 'trending-up', label: 'Trending Up', description: 'Strong upward momentum' },
    { value: 'trending-down', label: 'Trending Down', description: 'Strong downward momentum' },
    { value: 'ranging', label: 'Ranging', description: 'Sideways movement' },
    { value: 'volatile', label: 'Volatile', description: 'High price fluctuations' },
    { value: 'consolidating', label: 'Consolidating', description: 'Price compression' },
    { value: 'breakout', label: 'Breakout', description: 'Breaking key levels' }
  ];

  const volatilityOptions = [
    { value: 'low', label: 'Low Volatility', description: 'Calm market conditions' },
    { value: 'medium', label: 'Medium Volatility', description: 'Normal price movement' },
    { value: 'high', label: 'High Volatility', description: 'Significant price swings' },
    { value: 'extreme', label: 'Extreme Volatility', description: 'Unusual market activity' }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
      <Select
        label="Market Condition"
        description="Overall market trend during trade"
        options={marketConditionOptions}
        value={marketCondition}
        onChange={onConditionChange}
        placeholder="Select market condition"
        searchable
      />
      <Select
        label="Volatility Level"
        description="Price movement intensity"
        options={volatilityOptions}
        value={volatility}
        onChange={onVolatilityChange}
        placeholder="Select volatility level"
      />
    </div>
  );
};

export default MarketConditionAssessment;