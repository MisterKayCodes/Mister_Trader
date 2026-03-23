import React, { useState } from 'react';
import AuthenticatedHeader from '../../components/layout/AuthenticatedHeader';
import PrimaryNavigation from '../../components/layout/PrimaryNavigation';
import AccountContextBar from '../../components/layout/AccountContextBar';
import OverviewTab from './components/OverviewTab';
import SessionsTab from './components/SessionsTab';
import StrategiesTab from './components/StrategiesTab';
import PairsTab from './components/PairsTab';
import DaysTab from './components/DaysTab';
import PsychologyTab from './components/PsychologyTab';
import TimeTab from './components/TimeTab';
import StreakTab from './components/StreakTab';
import RefreshTab from './components/RefreshTab';
import Icon from '../../components/AppIcon';

const Analytics = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedAccount, setSelectedAccount] = useState('');

  const tabs = [
    { id: 'overview', label: 'Overview', icon: 'LayoutDashboard' },
    { id: 'sessions', label: 'Sessions', icon: 'Clock' },
    { id: 'strategies', label: 'Strategies', icon: 'Target' },
    { id: 'pairs', label: 'Pairs', icon: 'TrendingUp' },
    { id: 'days', label: 'Days', icon: 'Calendar' },
    { id: 'psychology', label: 'Psychology', icon: 'Brain' },
    { id: 'time', label: 'Time', icon: 'Timer' },
    { id: 'streak', label: 'Streak', icon: 'Zap' },
    { id: 'refresh', label: 'Refresh', icon: 'RefreshCw' }
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewTab selectedAccount={selectedAccount} />;
      case 'sessions':
        return <SessionsTab selectedAccount={selectedAccount} />;
      case 'strategies':
        return <StrategiesTab selectedAccount={selectedAccount} />;
      case 'pairs':
        return <PairsTab selectedAccount={selectedAccount} />;
      case 'days':
        return <DaysTab selectedAccount={selectedAccount} />;
      case 'psychology':
        return <PsychologyTab selectedAccount={selectedAccount} />;
      case 'time':
        return <TimeTab selectedAccount={selectedAccount} />;
      case 'streak':
        return <StreakTab selectedAccount={selectedAccount} />;
      case 'refresh':
        return <RefreshTab />;
      default:
        return <OverviewTab selectedAccount={selectedAccount} />;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <AuthenticatedHeader />
      <PrimaryNavigation />
      <AccountContextBar 
        selectedAccount={selectedAccount}
        onAccountChange={setSelectedAccount}
      />
      
      <main className="main-content">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="mb-6">
            <h1 className="text-2xl md:text-3xl font-bold text-foreground mb-2">Trading Analytics</h1>
            <p className="text-muted-foreground">Comprehensive performance analysis and insights</p>
          </div>

          {/* Tab Navigation */}
          <div className="bg-card border border-border rounded-lg mb-6 overflow-hidden">
            <div className="overflow-x-auto">
              <div className="flex border-b border-border min-w-max">
                {tabs?.map((tab) => (
                  <button
                    key={tab?.id}
                    onClick={() => setActiveTab(tab?.id)}
                    className={`flex items-center gap-2 px-4 md:px-6 py-3 md:py-4 text-sm md:text-base font-medium transition-colors whitespace-nowrap ${
                      activeTab === tab?.id
                        ? 'text-primary border-b-2 border-primary bg-primary/5' :'text-muted-foreground hover:text-foreground hover:bg-muted/50'
                    }`}
                  >
                    <Icon name={tab?.icon} size={18} />
                    <span>{tab?.label}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Tab Content */}
          <div className="animate-fadeIn">
            {renderTabContent()}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Analytics;