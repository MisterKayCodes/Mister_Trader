import React from 'react';
import Icon from '../../../components/AppIcon';

const SecurityBadges = () => {
  const securityFeatures = [
    {
      icon: 'Shield',
      text: '256-bit SSL Encryption'
    },
    {
      icon: 'Lock',
      text: 'Secure Authentication'
    },
    {
      icon: 'Database',
      text: 'Protected Data Storage'
    }
  ];

  return (
    <div className="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-6 pt-6 border-t border-border">
      {securityFeatures?.map((feature, index) => (
        <div
          key={index}
          className="flex items-center gap-2 text-muted-foreground"
        >
          <Icon name={feature?.icon} size={16} className="text-accent" />
          <span className="text-xs sm:text-sm font-medium">{feature?.text}</span>
        </div>
      ))}
    </div>
  );
};

export default SecurityBadges;