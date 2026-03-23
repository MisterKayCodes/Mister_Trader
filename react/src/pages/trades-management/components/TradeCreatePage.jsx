import React from 'react';
import AuthenticatedHeader from '../../../components/layout/AuthenticatedHeader';
import PrimaryNavigation from '../../../components/layout/PrimaryNavigation';
import AccountContextBar from '../../../components/layout/AccountContextBar';
import TradeCreateForm from './TradeCreateForm';

const TradeCreatePage = () => {
  const handleAccountChange = (accountId) => {
    // You can update selected account state or do other logic here
    console.log('Account changed:', accountId);
  };

  const handleTradeSuccess = () => {
    // Handle trade creation success (e.g., redirect, toast notification)
    console.log('Trade created successfully');
  };

  return (
    <div className="min-h-screen bg-background">
      <AuthenticatedHeader />
      <PrimaryNavigation />
      <AccountContextBar onAccountChange={handleAccountChange} />
      <main className="main-content with-account-context">
        <div className="main-content-container">
          <TradeCreateForm onSuccess={handleTradeSuccess} />
        </div>
      </main>
    </div>
  );
};

export default TradeCreatePage;
