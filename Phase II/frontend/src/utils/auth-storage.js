/**
 * Utility functions for handling JWT token storage and retrieval
 */

// Key for storing JWT token in localStorage
const TOKEN_KEY = 'jwt_token';

/**
 * Store JWT token in localStorage
 * @param {string} token - The JWT token to store
 */
export const storeToken = (token) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token);
  }
};

/**
 * Retrieve JWT token from localStorage
 * @returns {string|null} The stored JWT token or null if not found
 */
export const getToken = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
};

/**
 * Remove JWT token from localStorage
 */
export const removeToken = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
  }
};

/**
 * Check if a token exists and is valid
 * @returns {boolean} True if token exists and is not expired
 */
export const isTokenValid = () => {
  const token = getToken();
  if (!token) {
    return false;
  }

  try {
    // Decode the token to check its validity
    const payload = parseJwt(token);
    const currentTime = Math.floor(Date.now() / 1000);

    // Check if token is expired (compare expiration time with current time)
    return payload.exp > currentTime;
  } catch (error) {
    console.error('Error validating token:', error);
    return false;
  }
};

/**
 * Parse JWT token to extract payload
 * @param {string} token - The JWT token to parse
 * @returns {object} The decoded payload
 */
export const parseJwt = (token) => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  } catch (error) {
    throw new Error('Invalid token format');
  }
};

/**
 * Get user ID from JWT token
 * @returns {number|null} The user ID or null if not found
 */
export const getUserIdFromToken = () => {
  const token = getToken();
  if (!token) {
    return null;
  }

  try {
    const payload = parseJwt(token);
    return payload.user_id || null;
  } catch (error) {
    console.error('Error extracting user ID from token:', error);
    return null;
  }
};