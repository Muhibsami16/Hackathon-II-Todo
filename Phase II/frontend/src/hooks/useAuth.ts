import { useState, useEffect } from 'react';
import authService from '@/src/services/auth-service';

// Define the user type
interface User {
  id: number;
  email: string;
  // Add other user properties as needed
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true,
  });

  // Check authentication status on mount
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const token = authService.getCurrentToken();

        if (token && !authService.isTokenExpired()) {
          // In a real app, you might want to fetch user details using the token
          setAuthState({
            user: null, // In a real app, this would be populated with user data
            token,
            isAuthenticated: true,
            isLoading: false,
          });
        } else {
          setAuthState({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
          });
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        setAuthState({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
        });
      }
    };

    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    const result = await authService.login({ email, password });

    if (result.success) {
      const token = result.data?.access_token;
      if (token) {
        setAuthState({
          user: null, // In a real app, this would be populated with user data
          token,
          isAuthenticated: true,
          isLoading: false,
        });
      }
    }

    return result;
  };

  const register = async (email: string, password: string) => {
    const result = await authService.register({ email, password });
    return result;
  };

  const logout = async () => {
    await authService.logout();
    setAuthState({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
    });
  };

  return {
    ...authState,
    login,
    register,
    logout,
  };
};

export default useAuth;
