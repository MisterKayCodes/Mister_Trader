import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Icon from '../AppIcon';

const PrimaryNavigation = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigationItems = [
    {
      label: 'Dashboard',
      path: '/dashboard',
      icon: 'LayoutDashboard',
      tooltip: 'View performance overview and trading statistics'
    },
    {
      label: 'Accounts',
      path: '/accounts-management',
      icon: 'Wallet',
      tooltip: 'Manage trading accounts and configurations'
    },
    {
      label: 'Trades',
      path: '/trades-management',
      icon: 'TrendingUp',
      tooltip: 'Track and analyze individual trades'
    },
    {
      label: 'Psychology',
      path: '/trade-psychology-editor',
      icon: 'Brain',
      tooltip: 'Reflect on trading decisions and emotions'
    },
    {
      label: 'Analytics',
      path: '/trading-analytics-dashboard',
      icon: 'BarChart3',
      tooltip: 'Comprehensive performance analysis and insights'
    }
  ];

  useEffect(() => {
    const handleEscape = (event) => {
      if (event?.key === 'Escape' && isMobileMenuOpen) {
        setIsMobileMenuOpen(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isMobileMenuOpen]);

  useEffect(() => {
    if (isMobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [isMobileMenuOpen]);

  const handleNavigation = (path) => {
    navigate(path);
    setIsMobileMenuOpen(false);
  };

  const isActive = (path) => {
    return location?.pathname === path;
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <>
      <nav className="primary-navigation hidden lg:block">
        <div className="primary-navigation-content">
          <div className="primary-navigation-menu" role="navigation" aria-label="Primary navigation">
            {navigationItems?.map((item) => (
              <button
                key={item?.path}
                onClick={() => handleNavigation(item?.path)}
                className={`primary-navigation-item focus-ring ${isActive(item?.path) ? 'active' : ''}`}
                title={item?.tooltip}
                aria-current={isActive(item?.path) ? 'page' : undefined}
              >
                <Icon name={item?.icon} size={20} />
                <span>{item?.label}</span>
              </button>
            ))}
          </div>
        </div>
      </nav>
      <button
        onClick={toggleMobileMenu}
        className="primary-navigation-mobile-toggle focus-ring"
        aria-label={isMobileMenuOpen ? 'Close navigation menu' : 'Open navigation menu'}
        aria-expanded={isMobileMenuOpen}
      >
        <Icon name={isMobileMenuOpen ? "X" : "Menu"} size={24} />
      </button>
      {isMobileMenuOpen && (
        <div className="primary-navigation-mobile-menu">
          <div className="primary-navigation-mobile-menu-content" role="navigation" aria-label="Mobile navigation">
            {navigationItems?.map((item) => (
              <button
                key={item?.path}
                onClick={() => handleNavigation(item?.path)}
                className={`primary-navigation-mobile-item focus-ring ${isActive(item?.path) ? 'active' : ''}`}
                aria-current={isActive(item?.path) ? 'page' : undefined}
              >
                <Icon name={item?.icon} size={24} />
                <span>{item?.label}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </>
  );
};

export default PrimaryNavigation;