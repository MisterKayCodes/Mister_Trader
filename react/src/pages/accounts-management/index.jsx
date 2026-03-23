import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import api from '../../auth/api'; // Axios instance with auth
import AuthenticatedHeader from '../../components/layout/AuthenticatedHeader';
import PrimaryNavigation from '../../components/layout/PrimaryNavigation';
import AccountContextBar from '../../components/layout/AccountContextBar';
import Button from '../../components/ui/Button';
import AccountCard from './components/AccountCard';
import AccountFormModal from './components/AccountFormModal';
import DeleteConfirmModal from './components/DeleteConfirmModal';
import SearchFilterBar from './components/SearchFilterBar';
import EmptyState from './components/EmptyState';

const AccountsManagement = () => {
  const [accounts, setAccounts] = useState([]);
  const [filteredAccounts, setFilteredAccounts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  
  const [isFormModalOpen, setIsFormModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectedAccount, setSelectedAccount] = useState(null);
  const [formMode, setFormMode] = useState('create');
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    fetchAccounts();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [accounts, searchQuery]);

  const fetchAccounts = async () => {
    setIsLoading(true);
    try {
      const response = await api.get('/accounts');
      const data = response.data;
      setAccounts(data);
    } catch (err) {
      console.error("Failed to fetch accounts:", err);
      // Optional: Handle error UI
    } finally {
      setIsLoading(false);
    }
  };

  const applyFilters = () => {
    if (!accounts) return;
    let filtered = [...accounts];

    if (searchQuery?.trim()) {
      filtered = filtered.filter(account =>
        account?.name?.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredAccounts(filtered);
  };

  const handleAddAccount = () => {
    setFormMode('create');
    setSelectedAccount(null);
    setIsFormModalOpen(true);
  };

  const handleEditAccount = (account) => {
    setFormMode('edit');
    setSelectedAccount(account);
    setIsFormModalOpen(true);
  };

  const handleDeleteAccount = (account) => {
    setSelectedAccount(account);
    setIsDeleteModalOpen(true);
  };

  const handleFormSubmit = async (formData) => {
    try {
      if (formMode === 'create') {
        // Send POST request
        const response = await api.post('/accounts', { name: formData.name });
        // Add new account to the state
        setAccounts(prev => [response.data, ...prev]);
      } else {
        // Send PUT request
        const response = await api.put(`/accounts/${formData.id}`, { name: formData.name });
        // Update account in the state
        setAccounts(prev =>
          prev.map(acc => acc.id === formData.id ? { ...acc, ...response.data } : acc)
        );
      }
      setIsFormModalOpen(false);
      setSelectedAccount(null);
    } catch (err) {
      console.error("Failed to save account:", err);
      alert(err.response?.data?.detail || "Failed to save account. Please verify input and try again.");
    }
  };

  const handleConfirmDelete = async () => {
    if (!selectedAccount) return;
    setIsDeleting(true);
    
    try {
      // Send DELETE request
      await api.delete(`/accounts/${selectedAccount.id}`);
      
      // Remove from UI state
      setAccounts(prev => prev.filter(acc => acc.id !== selectedAccount.id));
      
      setIsDeleting(false);
      setIsDeleteModalOpen(false);
      setSelectedAccount(null);
    } catch (err) {
      console.error("Failed to delete account:", err);
      alert(err.response?.data?.detail || "Failed to delete account.");
      setIsDeleting(false);
    }
  };

  const hasActiveFilters = searchQuery?.trim() !== '';

  return (
    <>
      <Helmet>
        <title>Accounts Management - TradingJournal</title>
        <meta name="description" content="Manage your trading accounts, create vaults, and organize your trades." />
      </Helmet>
      <AuthenticatedHeader />
      <PrimaryNavigation />
      <AccountContextBar />
      <main className="main-content with-account-context">
        <div className="main-content-container space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-2 md:mb-4">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-foreground mb-2">
                Trading Accounts
              </h1>
              <p className="text-sm md:text-base text-muted-foreground">
                Manage and monitor all your trading accounts in one place
              </p>
            </div>
            <Button
              variant="default"
              onClick={handleAddAccount}
              iconName="Plus"
              iconPosition="left"
              className="sm:flex-shrink-0"
            >
              Add New Account
            </Button>
          </div>

          <SearchFilterBar
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
          />

          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 mt-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-card border border-border rounded-lg p-6 animate-pulse">
                  <div className="flex items-start gap-3 mb-4">
                    <div className="w-12 h-12 bg-muted rounded-lg"></div>
                    <div className="flex-1">
                      <div className="h-5 bg-muted rounded w-3/4 mb-2"></div>
                      <div className="h-4 bg-muted rounded w-1/2"></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : filteredAccounts?.length === 0 ? (
            <div className="mt-6">
              <EmptyState onAddAccount={handleAddAccount} hasFilters={hasActiveFilters} />
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 mt-6">
              {filteredAccounts.map((account) => (
                <AccountCard
                  key={account.id}
                  account={account}
                  onEdit={handleEditAccount}
                  onDelete={handleDeleteAccount}
                />
              ))}
            </div>
          )}

          {!isLoading && filteredAccounts?.length > 0 && (
            <div className="mt-8 p-4 bg-muted/50 rounded-lg border border-border">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div className="text-sm text-muted-foreground">
                  Showing <span className="font-medium text-foreground">{filteredAccounts.length}</span> of{' '}
                  <span className="font-medium text-foreground">{accounts.length}</span> accounts
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
      <AccountFormModal
        isOpen={isFormModalOpen}
        onClose={() => {
          setIsFormModalOpen(false);
          setSelectedAccount(null);
        }}
        onSubmit={handleFormSubmit}
        account={selectedAccount}
        mode={formMode}
      />
      <DeleteConfirmModal
        isOpen={isDeleteModalOpen}
        onClose={() => {
          setIsDeleteModalOpen(false);
          setSelectedAccount(null);
        }}
        onConfirm={handleConfirmDelete}
        account={selectedAccount}
        isDeleting={isDeleting}
      />
    </>
  );
};

export default AccountsManagement;