import apiClient from './api-client';

class AuthService {
  // Check if user is authenticated
  isAuthenticated() {
    const token = apiClient.getToken();
    return !!token;
  }

  // Register a new user
  async register(userData: { email: string; password: string }) {
    try {
      const response = await apiClient.register(userData);
      return { success: true, data: response };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  // Login user
  async login(credentials: { email: string; password: string }) {
    try {
      const response = await apiClient.login(credentials);
      return { success: true, data: response };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  // Logout user
  async logout() {
    try {
      await apiClient.logout();
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.message };
    }
  }

  // Check if token is expired
  isTokenExpired() {
    const token = this.getCurrentToken();
    if (!token) return true;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const currentTime = Math.floor(Date.now() / 1000);
      return payload.exp < currentTime;
    } catch (error) {
      console.error('Error checking token expiration:', error);
      return true;
    }
  }

  // Get current user token
  getCurrentToken() {
    return apiClient.getToken();
  }

  // Refresh token if needed (not implemented in this basic version)
  async refreshToken() {
    // In a real implementation, this would call a refresh endpoint
    // For now, we'll just return the current token
    return apiClient.getToken();
  }
}

// Create singleton instance
const authService = new AuthService();

export default authService;
