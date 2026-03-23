import React from 'react';
import Icon from '../../../components/AppIcon';

const TemplatePrompts = ({ onTemplateSelect }) => {
  const templates = [
    {
      id: 'comprehensive',
      name: 'Comprehensive Analysis',
      icon: 'FileText',
      sections: [
        { title: 'Pre-Trade Mindset', prompt: 'What was my mental state before entering this trade? Was I calm, anxious, or overconfident?' },
        { title: 'Decision Process', prompt: 'What factors influenced my decision to enter? Did I follow my trading plan?' },
        { title: 'Execution Experience', prompt: 'How did I feel during the trade? Did I experience fear, greed, or discipline?' },
        { title: 'What Went Well', prompt: 'What aspects of this trade demonstrated good trading psychology and discipline?' },
        { title: 'Areas for Improvement', prompt: 'What could I have done differently? What mistakes did I make?' },
        { title: 'Key Lessons Learned', prompt: 'What specific insights can I apply to future trades?' }
      ]
    },
    {
      id: 'quick-reflection',
      name: 'Quick Reflection',
      icon: 'Zap',
      sections: [
        { title: 'Emotional State', prompt: 'How did I feel during this trade?' },
        { title: 'Decision Quality', prompt: 'Did I follow my plan? Why or why not?' },
        { title: 'Key Takeaway', prompt: 'What is the one thing I learned from this trade?' }
      ]
    },
    {
      id: 'mistake-analysis',
      name: 'Mistake Analysis',
      icon: 'AlertTriangle',
      sections: [
        { title: 'What Went Wrong', prompt: 'Describe the mistake or poor decision made during this trade.' },
        { title: 'Root Cause', prompt: 'What psychological factors led to this mistake? (Fear, greed, impatience, etc.)' },
        { title: 'Prevention Strategy', prompt: 'How can I prevent this mistake in future trades?' },
        { title: 'Action Plan', prompt: 'What specific steps will I take to improve?' }
      ]
    },
    {
      id: 'winning-trade',
      name: 'Winning Trade Review',
      icon: 'Trophy',
      sections: [
        { title: 'Success Factors', prompt: 'What did I do right in this trade?' },
        { title: 'Discipline Assessment', prompt: 'Did I stick to my plan? How did I manage emotions?' },
        { title: 'Replication Strategy', prompt: 'How can I replicate this success in future trades?' }
      ]
    }
  ];

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-foreground">
        Analysis Templates
      </label>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">
        {templates?.map((template) => (
          <button
            key={template?.id}
            type="button"
            onClick={() => onTemplateSelect(template)}
            className="flex items-start gap-3 p-4 md:p-5 bg-card border border-border rounded-lg hover:border-accent/50 hover:bg-accent/5 active:scale-[0.98] transition-all duration-250 text-left group"
          >
            <div className="flex-shrink-0 w-10 h-10 md:w-12 md:h-12 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors duration-250">
              <Icon name={template?.icon} size={20} className="text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <h4 className="text-sm md:text-base font-semibold text-foreground mb-1">{template?.name}</h4>
              <p className="text-xs md:text-sm text-muted-foreground line-clamp-2">
                {template?.sections?.length} guided sections
              </p>
            </div>
            <Icon name="ChevronRight" size={18} className="text-muted-foreground group-hover:text-primary transition-colors duration-250 flex-shrink-0" />
          </button>
        ))}
      </div>
    </div>
  );
};

export default TemplatePrompts;