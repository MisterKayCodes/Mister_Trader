import React, { useState } from 'react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import Icon from '../../../components/AppIcon';

const PerformanceChart = ({ data, loading }) => {
  const [timeframe, setTimeframe] = useState('1M');
  const [chartType, setChartType] = useState('line');

  const timeframes = [
    { label: '1W', value: '1W' },
    { label: '1M', value: '1M' },
    { label: '3M', value: '3M' },
    { label: '6M', value: '6M' },
    { label: '1Y', value: '1Y' },
    { label: 'ALL', value: 'ALL' }
  ];

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload?.length) {
      return (
        <div className="bg-popover border border-border rounded-lg p-3 shadow-lg">
          <p className="text-sm font-medium text-foreground mb-2">{label}</p>
          {payload?.map((entry, index) => (
            <div key={index} className="flex items-center gap-2">
              <div 
                className="w-3 h-3 rounded-full" 
                style={{ backgroundColor: entry?.color }}
              ></div>
              <span className="text-xs text-muted-foreground">{entry?.name}:</span>
              <span className="text-sm font-semibold text-foreground data-text">
                ${entry?.value?.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="bg-card border border-border rounded-lg p-4 md:p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="h-6 bg-muted rounded w-40"></div>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5, 6]?.map((i) => (
              <div key={i} className="h-8 w-12 bg-muted rounded"></div>
            ))}
          </div>
        </div>
        <div className="h-64 md:h-80 bg-muted rounded animate-pulse"></div>
      </div>
    );
  }

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div className="flex items-center gap-3">
          <h2 className="text-lg md:text-xl font-semibold text-foreground">Performance Overview</h2>
          <div className="flex items-center gap-2 bg-muted rounded-lg p-1">
            <button
              onClick={() => setChartType('line')}
              className={`p-1.5 rounded transition-smooth ${
                chartType === 'line' ?'bg-card shadow-sm' :'hover:bg-card/50'
              }`}
              title="Line Chart"
            >
              <Icon name="LineChart" size={16} className={chartType === 'line' ? 'text-primary' : 'text-muted-foreground'} />
            </button>
            <button
              onClick={() => setChartType('area')}
              className={`p-1.5 rounded transition-smooth ${
                chartType === 'area' ?'bg-card shadow-sm' :'hover:bg-card/50'
              }`}
              title="Area Chart"
            >
              <Icon name="AreaChart" size={16} className={chartType === 'area' ? 'text-primary' : 'text-muted-foreground'} />
            </button>
          </div>
        </div>

        <div className="flex gap-2 overflow-x-auto scrollbar-custom">
          {timeframes?.map((tf) => (
            <button
              key={tf?.value}
              onClick={() => setTimeframe(tf?.value)}
              className={`px-3 py-1.5 text-xs md:text-sm font-medium rounded-lg transition-smooth whitespace-nowrap flex-shrink-0 ${
                timeframe === tf?.value
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted text-muted-foreground hover:bg-muted/80'
              }`}
            >
              {tf?.label}
            </button>
          ))}
        </div>
      </div>
      <div className="w-full h-64 md:h-80" aria-label="Trading Performance Chart">
        <ResponsiveContainer width="100%" height="100%">
          {chartType === 'line' ? (
            <LineChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
              <XAxis 
                dataKey="date" 
                stroke="var(--color-muted-foreground)"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="var(--color-muted-foreground)"
                style={{ fontSize: '12px' }}
                tickFormatter={(value) => `$${(value / 1000)?.toFixed(0)}k`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                wrapperStyle={{ fontSize: '12px' }}
                iconType="circle"
              />
              <Line 
                type="monotone" 
                dataKey="balance" 
                stroke="var(--color-primary)" 
                strokeWidth={2}
                dot={{ fill: 'var(--color-primary)', r: 4 }}
                activeDot={{ r: 6 }}
                name="Account Balance"
              />
              <Line 
                type="monotone" 
                dataKey="profit" 
                stroke="var(--color-success)" 
                strokeWidth={2}
                dot={{ fill: 'var(--color-success)', r: 4 }}
                activeDot={{ r: 6 }}
                name="Cumulative Profit"
              />
            </LineChart>
          ) : (
            <AreaChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
              <defs>
                <linearGradient id="colorBalance" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--color-primary)" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="var(--color-primary)" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorProfit" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--color-success)" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="var(--color-success)" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
              <XAxis 
                dataKey="date" 
                stroke="var(--color-muted-foreground)"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="var(--color-muted-foreground)"
                style={{ fontSize: '12px' }}
                tickFormatter={(value) => `$${(value / 1000)?.toFixed(0)}k`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                wrapperStyle={{ fontSize: '12px' }}
                iconType="circle"
              />
              <Area 
                type="monotone" 
                dataKey="balance" 
                stroke="var(--color-primary)" 
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorBalance)"
                name="Account Balance"
              />
              <Area 
                type="monotone" 
                dataKey="profit" 
                stroke="var(--color-success)" 
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorProfit)"
                name="Cumulative Profit"
              />
            </AreaChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PerformanceChart;