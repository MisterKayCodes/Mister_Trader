import React from 'react';
import Icon from '../../components/AppIcon';
import LoginForm from './components/LoginForm';
import SecurityBadges from './components/SecurityBadges';
import RegisterPrompt from './components/RegisterPrompt';

const Login = () => {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4 sm:p-6 lg:p-8">
      <div className="w-full max-w-md">
        <div className="bg-card rounded-lg shadow-lg border border-border p-6 sm:p-8 lg:p-10">
          <div className="flex flex-col items-center mb-8">
            <div
              className="w-16 h-16 sm:w-20 sm:h-20 rounded-lg flex items-center justify-center mb-4"
              style={{ background: 'linear-gradient(135deg, var(--color-primary), var(--color-secondary))' }}
            >
              <Icon name="TrendingUp" size={32} color="#FFFFFF" />
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground text-center">Welcome Back</h1>
            <p className="text-sm sm:text-base text-muted-foreground text-center mt-2">
              Sign in to access your trading journal
            </p>
          </div>

          <LoginForm />

          <div className="mt-8">
            <RegisterPrompt />
          </div>

          <div className="mt-8">
            <SecurityBadges />
          </div>
        </div>

        <div className="mt-6 text-center">
          <p className="text-xs text-muted-foreground">
            By signing in, you agree to our Terms of Service and Privacy Policy
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
