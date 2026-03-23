import React from 'react';
import { useNavigate } from 'react-router-dom';
import Icon from '../../../components/AppIcon';


const QuickActions = () => {
  const navigate = useNavigate();

  const actions = [
    {
      id: 1,
      title: "Add New Trade",
      description: "Record your latest trading activity",
      icon: "Plus",
      iconColor: "var(--color-success)",
      onClick: () => navigate('/trades-management')
    },
    {
      id: 2,
      title: "Manage Accounts",
      description: "View and edit trading accounts",
      icon: "Wallet",
      iconColor: "var(--color-primary)",
      onClick: () => navigate('/accounts-management')
    },
    {
      id: 3,
      title: "Psychology Notes",
      description: "Reflect on trading decisions",
      icon: "Brain",
      iconColor: "var(--color-accent)",
      onClick: () => navigate('/trade-psychology-editor')
    }
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-4 md:p-6">
      <h2 className="text-lg md:text-xl font-semibold text-foreground mb-4">Quick Actions</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4">
        {actions?.map((action) => (
          <button
            key={action?.id}
            onClick={action?.onClick}
            className="flex items-start gap-4 p-4 rounded-lg border border-border hover:border-primary hover:bg-accent/5 transition-smooth text-left group"
          >
            <div 
              className="w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-smooth"
              style={{ backgroundColor: `${action?.iconColor}15` }}
            >
              <Icon name={action?.icon} size={24} color={action?.iconColor} />
            </div>
            
            <div className="flex-1 min-w-0">
              <h3 className="text-sm md:text-base font-semibold text-foreground mb-1 group-hover:text-primary transition-smooth">
                {action?.title}
              </h3>
              <p className="text-xs md:text-sm text-muted-foreground line-clamp-2">
                {action?.description}
              </p>
            </div>
            
            <Icon 
              name="ArrowRight" 
              size={20} 
              className="text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-smooth flex-shrink-0"
            />
          </button>
        ))}
      </div>
    </div>
  );
};

export default QuickActions;