import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import AuthenticatedHeader from '../../components/layout/AuthenticatedHeader';
import PrimaryNavigation from '../../components/layout/PrimaryNavigation';
import AccountContextBar from '../../components/layout/AccountContextBar';
import Button from '../../components/ui/Button';
import TradeList from './components/TradeList';

// Use environment variable for API base URL or fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api/v1';

const TradesManagement = () => {
  const navigate = useNavigate();
  const [selectedAccount, setSelectedAccount] = useState('');
  const [trades, setTrades] = useState([]);
  const [filteredTrades, setFilteredTrades] = useState([]);
  const [loading, setLoading] = useState(false);

  // Get auth token from localStorage
  const getToken = () => localStorage.getItem('access_token');

  // Fetch trades for selected account
  useEffect(() => {
    if (!selectedAccount) {
      setTrades([]);
      setFilteredTrades([]);
      return;
    }

    const fetchTrades = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`${API_BASE_URL}/trades`, {
          params: { account_id: selectedAccount },
          headers: { Authorization: `Bearer ${getToken()}` }
        });
        setTrades(response.data);
        setFilteredTrades(response.data);
      } catch (error) {
        console.error('Error fetching trades:', error);
        setTrades([]);
        setFilteredTrades([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTrades();
  }, [selectedAccount]);

  // Handle account change from AccountContextBar
  const handleAccountChange = (accountId) => {
    setSelectedAccount(accountId);
  };

  // Filter trades based on filter criteria
  const handleFilterChange = (filters) => {
    let filtered = [...trades];

    if (filters?.dateFrom) {
      filtered = filtered.filter(trade => trade?.open_timestamp >= filters.dateFrom);
    }
    if (filters?.dateTo) {
      filtered = filtered.filter(trade => trade?.open_timestamp <= filters.dateTo);
    }
    if (filters?.symbol) {
      filtered = filtered.filter(trade => trade?.symbol.toLowerCase().includes(filters.symbol.toLowerCase()));
    }
    if (filters?.tradeType) {
      filtered = filtered.filter(trade => trade?.side === filters.tradeType);
    }
    if (filters?.profitLossMin) {
      filtered = filtered.filter(trade => trade?.pnl >= parseFloat(filters.profitLossMin));
    }
    if (filters?.profitLossMax) {
      filtered = filtered.filter(trade => trade?.pnl <= parseFloat(filters.profitLossMax));
    }
    if (filters?.tags && filters.tags.length > 0) {
      filtered = filtered.filter(trade => filters.tags.some(tag => trade.notes?.includes(tag)));
    }

    setFilteredTrades(filtered);
  };

  // Delete trade by id
  const handleDeleteTrade = async (trade) => {
    if (!window.confirm(`Are you sure you want to delete trade ${trade.symbol}?`)) return;

    try {
      await axios.delete(`${API_BASE_URL}/trades/${trade.id}`, {
        headers: { Authorization: `Bearer ${getToken()}` }
      });
      // Remove deleted trade from state
      const updatedTrades = trades.filter(t => t.id !== trade.id);
      setTrades(updatedTrades);
      setFilteredTrades(filteredTrades.filter(t => t.id !== trade.id));
    } catch (error) {
      console.error('Failed to delete trade:', error);
      alert('Failed to delete trade');
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <AuthenticatedHeader />
      <PrimaryNavigation />
      <AccountContextBar onAccountChange={handleAccountChange} />
      <main className="main-content with-account-context">
        <div className="main-content-container">
          <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 mb-6">
            <div>
              <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold text-foreground mb-2">
                Trades Management
              </h1>
              <p className="text-sm md:text-base text-muted-foreground">
                Track and analyze your trading performance with detailed trade records
              </p>
            </div>
            <Button
              variant="default"
              size="lg"
              iconName="Plus"
              iconPosition="left"
              onClick={() => navigate('/trades-management/create')}
            >
              Add New Trade
            </Button>
          </div>

          <TradeList
            trades={filteredTrades}
            onFilterChange={handleFilterChange}
            onDelete={handleDeleteTrade}
            loading={loading}
          />
        </div>
      </main>
    </div>
  );
};

export default TradesManagement;
