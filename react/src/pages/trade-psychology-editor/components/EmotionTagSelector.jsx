import React from 'react';
import Icon from '../../../components/AppIcon';

const EmotionTagSelector = ({ selectedEmotions, onEmotionToggle }) => {
  const emotionTags = [
    { id: 'fear', label: 'Fear', icon: 'AlertTriangle', color: 'text-error', bgColor: 'bg-error/10', borderColor: 'border-error/20' },
    { id: 'greed', label: 'Greed', icon: 'TrendingUp', color: 'text-warning', bgColor: 'bg-warning/10', borderColor: 'border-warning/20' },
    { id: 'confidence', label: 'Confidence', icon: 'Award', color: 'text-success', bgColor: 'bg-success/10', borderColor: 'border-success/20' },
    { id: 'uncertainty', label: 'Uncertainty', icon: 'HelpCircle', color: 'text-muted-foreground', bgColor: 'bg-muted', borderColor: 'border-border' },
    { id: 'excitement', label: 'Excitement', icon: 'Zap', color: 'text-primary', bgColor: 'bg-primary/10', borderColor: 'border-primary/20' },
    { id: 'frustration', label: 'Frustration', icon: 'Frown', color: 'text-destructive', bgColor: 'bg-destructive/10', borderColor: 'border-destructive/20' },
    { id: 'calm', label: 'Calm', icon: 'Smile', color: 'text-accent', bgColor: 'bg-accent/10', borderColor: 'border-accent/20' },
    { id: 'anxiety', label: 'Anxiety', icon: 'AlertCircle', color: 'text-orange-500', bgColor: 'bg-orange-500/10', borderColor: 'border-orange-500/20' }
  ];

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-foreground">
        Emotional State
      </label>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 md:gap-3">
        {emotionTags?.map((emotion) => {
          const isSelected = selectedEmotions?.includes(emotion?.id);
          return (
            <button
              key={emotion?.id}
              type="button"
              onClick={() => onEmotionToggle(emotion?.id)}
              className={`flex items-center gap-2 px-3 md:px-4 py-2 md:py-3 rounded-lg border-2 transition-all duration-250 ${
                isSelected
                  ? `${emotion?.bgColor} ${emotion?.borderColor} ${emotion?.color}`
                  : 'bg-card border-border text-muted-foreground hover:border-accent/30'
              }`}
              aria-pressed={isSelected}
            >
              <Icon name={emotion?.icon} size={18} className="flex-shrink-0" />
              <span className="text-xs md:text-sm font-medium truncate">{emotion?.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default EmotionTagSelector;