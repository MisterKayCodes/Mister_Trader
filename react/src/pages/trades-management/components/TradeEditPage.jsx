import React from 'react';
import AuthenticatedHeader from '../../../components/layout/AuthenticatedHeader';
import PrimaryNavigation from '../../../components/layout/PrimaryNavigation';
import AccountContextBar from '../../../components/layout/AccountContextBar';
import TradeEditForm from './TradeEditForm';

const TradeEditPage = () => {
  const handleAccountChange = (accountId) => {
    console.log('Account changed:', accountId);
    // Add any additional logic if needed
  };

  const handleTradeSuccess = () => {
    console.log('Trade edited successfully');
    // Add any post-success logic here (e.g., notifications, redirect)
  };

  return (
    <div className="min-h-screen bg-background">
      <AuthenticatedHeader />
      <PrimaryNavigation />
      <AccountContextBar onAccountChange={handleAccountChange} />
      <main className="main-content with-account-context">
        <div className="main-content-container">
          <TradeEditForm onSuccess={handleTradeSuccess} />
        </div>
      </main>
    </div>
  );
};

export default TradeEditPage;
