import React from 'react';
import AuthenticatedHeader from '../../../components/layout/AuthenticatedHeader';
import PrimaryNavigation from '../../../components/layout/PrimaryNavigation';
import AccountContextBar from '../../../components/layout/AccountContextBar';
import TradeDetailsView from './TradeDetailsView';

const TradeDetailsPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <AuthenticatedHeader />
      <PrimaryNavigation />
      <AccountContextBar />
      <main className="main-content with-account-context">
        <div className="main-content-container">
          <TradeDetailsView />
        </div>
      </main>
    </div>
  );
};

export default TradeDetailsPage;
