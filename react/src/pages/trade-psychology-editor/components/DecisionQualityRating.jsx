import React from 'react';
import Icon from '../../../components/AppIcon';

const DecisionQualityRating = ({ rating, onRatingChange }) => {
  const ratingLevels = [
    { value: 1, label: 'Poor', color: 'text-error', bgColor: 'bg-error/10', icon: 'ThumbsDown' },
    { value: 2, label: 'Below Average', color: 'text-warning', bgColor: 'bg-warning/10', icon: 'TrendingDown' },
    { value: 3, label: 'Average', color: 'text-muted-foreground', bgColor: 'bg-muted', icon: 'Minus' },
    { value: 4, label: 'Good', color: 'text-accent', bgColor: 'bg-accent/10', icon: 'TrendingUp' },
    { value: 5, label: 'Excellent', color: 'text-success', bgColor: 'bg-success/10', icon: 'ThumbsUp' }
  ];

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-foreground">
        Decision Quality Rating
      </label>
      <div className="grid grid-cols-1 md:grid-cols-5 gap-2 md:gap-3">
        {ratingLevels?.map((level) => {
          const isSelected = rating === level?.value;
          return (
            <button
              key={level?.value}
              type="button"
              onClick={() => onRatingChange(level?.value)}
              className={`flex flex-col items-center gap-2 px-3 md:px-4 py-3 md:py-4 rounded-lg border-2 transition-all duration-250 ${
                isSelected
                  ? `${level?.bgColor} border-current ${level?.color}`
                  : 'bg-card border-border text-muted-foreground hover:border-accent/30'
              }`}
              aria-pressed={isSelected}
            >
              <Icon name={level?.icon} size={24} />
              <span className="text-xs md:text-sm font-medium text-center">{level?.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default DecisionQualityRating;