import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../../../components/ui/Button';

const RegisterPrompt = () => {
  const navigate = useNavigate();

  const handleRegisterClick = () => {
    navigate('/register');
  };

  return (
    <div className="text-center space-y-4">
      <p className="text-sm text-muted-foreground">
        Don't have an account?
      </p>
      <Button
        variant="outline"
        fullWidth
        onClick={handleRegisterClick}
        iconName="UserPlus"
        iconPosition="left"
      >
        Create New Account
      </Button>
    </div>
  );
};

export default RegisterPrompt;