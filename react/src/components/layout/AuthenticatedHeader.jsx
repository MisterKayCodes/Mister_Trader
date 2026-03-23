import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Icon from '../AppIcon';
import { useTheme } from '../ThemeProvider';
import api from '../../auth/api';

const AuthenticatedHeader = () => {
  const navigate = useNavigate();
  const { theme, setTheme } = useTheme();
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);
  const userMenuRef = useRef(null);

  const [currentUser, setCurrentUser] = useState({
    name: 'Loading...',
    email: '',
    initials: 'TG'
  });

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get('/users/me');
        const user = response.data;
        setCurrentUser({
          name: `TG: ${user.telegram_user_id}`,
          email: 'Telegram Account',
          initials: user.telegram_user_id.toString().substring(0, 2)
        });
      } catch (err) {
        console.error('Failed to fetch user profile:', err);
        setCurrentUser({
          name: 'Unknown User',
          email: 'Not Logged In',
          initials: '??'
        });
      }
    };
    fetchUser();
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (userMenuRef?.current && !userMenuRef?.current?.contains(event?.target)) {
        setIsUserMenuOpen(false);
      }
    };

    const handleEscape = (event) => {
      if (event?.key === 'Escape') {
        setIsUserMenuOpen(false);
      }
    };

    if (isUserMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleEscape);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isUserMenuOpen]);

  const handleLogout = () => {
    setIsUserMenuOpen(false);
    navigate('/login');
  };

  const handleProfile = () => {
    setIsUserMenuOpen(false);
  };

  const toggleUserMenu = () => {
    setIsUserMenuOpen(!isUserMenuOpen);
  };

  return (
    <header className="authenticated-header">
      <div className="authenticated-header-content">
        <div className="authenticated-header-logo">
          <div className="authenticated-header-logo-icon">
            <Icon name="TrendingUp" size={24} color="#FFFFFF" />
          </div>
          <span className="authenticated-header-logo-text">MisterTrader</span>
        </div>

        <div className="authenticated-header-actions">
          <button
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            className="p-2 mr-2 rounded-full text-muted-foreground hover:bg-muted focus:outline-none focus:ring-2 focus:ring-primary/50 transition-colors"
            title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
          >
            <Icon name={theme === 'dark' ? 'Sun' : 'Moon'} size={20} />
          </button>

          <div className="relative" ref={userMenuRef}>
            <button
              onClick={toggleUserMenu}
              className="authenticated-header-user focus-ring"
              aria-expanded={isUserMenuOpen}
              aria-haspopup="true"
            >
              <div className="authenticated-header-user-avatar">
                {currentUser?.initials}
              </div>
              <div className="authenticated-header-user-info">
                <div className="authenticated-header-user-name">
                  {currentUser?.name}
                </div>
                <div className="authenticated-header-user-email">
                  {currentUser?.email}
                </div>
              </div>
              <Icon 
                name={isUserMenuOpen ? "ChevronUp" : "ChevronDown"} 
                size={20} 
                className="text-muted-foreground transition-smooth"
              />
            </button>

            {isUserMenuOpen && (
              <div 
                className="absolute right-0 mt-2 w-64 bg-popover border border-border rounded-lg shadow-lg overflow-hidden z-[1100]"
                role="menu"
              >
                <div className="p-4 border-b border-border">
                  <div className="font-medium text-foreground">{currentUser?.name}</div>
                  <div className="text-sm text-muted-foreground">{currentUser?.email}</div>
                </div>
                
                <div className="py-2">
                  <button
                    onClick={handleProfile}
                    className="w-full px-4 py-3 text-left flex items-center gap-3 hover:bg-muted transition-smooth text-foreground"
                    role="menuitem"
                  >
                    <Icon name="User" size={18} />
                    <span className="text-sm font-medium">Profile Settings</span>
                  </button>
                  
                  <button
                    onClick={handleLogout}
                    className="w-full px-4 py-3 text-left flex items-center gap-3 hover:bg-muted transition-smooth text-destructive"
                    role="menuitem"
                  >
                    <Icon name="LogOut" size={18} />
                    <span className="text-sm font-medium">Logout</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default AuthenticatedHeader;