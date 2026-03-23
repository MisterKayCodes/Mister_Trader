import React, { useState, useEffect } from 'react';
import Select from '../ui/Select';

const AccountContextBar = ({ onAccountChange }) => {
  const [selectedAccount, setSelectedAccount] = useState('');
  const [accounts, setAccounts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAccounts = async () => {
      setIsLoading(true);
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          throw new Error('No access token found. Please log in.');
        }

        const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/accounts`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to fetch accounts');
        }

        const data = await response.json();

        // Map backend accounts to Select component options format
        const formattedAccounts = data.map(acc => ({
          value: acc.id.toString(),
          label: acc.name,
          description: '' // optionally add description if available
        }));

        setAccounts(formattedAccounts);

        if (formattedAccounts.length > 0) {
          let initialId = formattedAccounts[0].value;
          const savedId = localStorage.getItem('selected_account_id');
          if (savedId && formattedAccounts.some(acc => acc.value === savedId)) {
             initialId = savedId;
          }
          setSelectedAccount(initialId);
          localStorage.setItem('selected_account_id', initialId);
          
          if (onAccountChange) {
            onAccountChange(initialId);
          }
        }
      } catch (error) {
        alert(error.message);
        setAccounts([]);
        setSelectedAccount('');
        if (onAccountChange) {
          onAccountChange('');
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchAccounts();
  }, [onAccountChange]);

  const handleAccountChange = (value) => {
    setSelectedAccount(value);
    localStorage.setItem('selected_account_id', value);
    if (onAccountChange) {
      onAccountChange(value);
    }
  };

  return (
    <div className="account-context-bar">
      <div className="account-context-bar-content">
        <span className="account-context-bar-label">Trading Account:</span>
        <div className="account-context-bar-select">
          <Select
            options={accounts}
            value={selectedAccount}
            onChange={handleAccountChange}
            placeholder="Select trading account"
            loading={isLoading}
            searchable
            disabled={isLoading || accounts.length === 0}
          />
        </div>
      </div>
    </div>
  );
};

export default AccountContextBar;
