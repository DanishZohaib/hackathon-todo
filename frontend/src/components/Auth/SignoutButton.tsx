import React from "react";
import { useAuth } from "../../hooks/useAuth";
import Button from "../UI/Button";

interface SignoutButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const SignoutButton: React.FC<SignoutButtonProps> = ({
  variant = 'outline',
  size = 'md',
  className = ''
}) => {
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <Button
      variant={variant}
      size={size}
      className={className}
      onClick={handleLogout}
    >
      Sign Out
    </Button>
  );
};

export default SignoutButton;