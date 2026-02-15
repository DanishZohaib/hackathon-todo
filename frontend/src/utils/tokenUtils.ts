// Utility functions for handling JWT tokens

/**
 * Decodes a JWT token to extract its payload
 * @param token The JWT token to decode
 * @returns The decoded payload or null if invalid
 */
export const decodeToken = (token: string): any | null => {
  try {
    // Split the token to get the payload part (middle part)
    const parts = token.split('.');
    if (parts.length !== 3) {
      console.error('Invalid token format');
      return null;
    }

    // Decode the payload (second part)
    const payload = parts[1];
    // Add padding if needed
    const paddedPayload = payload + '='.repeat((4 - (payload.length % 4)) % 4);
    const decodedPayload = atob(paddedPayload);
    return JSON.parse(decodedPayload);
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

/**
 * Checks if a JWT token is expired
 * @param token The JWT token to check
 * @returns True if expired, false otherwise
 */
export const isTokenExpired = (token: string): boolean => {
  const payload = decodeToken(token);
  if (!payload || !payload.exp) {
    return true; // If there's no expiration, consider it expired
  }

  const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
  return payload.exp < currentTime;
};

/**
 * Gets the expiration time from a JWT token
 * @param token The JWT token to check
 * @returns The expiration timestamp or null if not available
 */
export const getTokenExpiration = (token: string): number | null => {
  const payload = decodeToken(token);
  if (!payload || !payload.exp) {
    return null;
  }
  return payload.exp;
};

/**
 * Checks if a token is valid (exists and not expired)
 * @param token The JWT token to check
 * @returns True if valid, false otherwise
 */
export const isValidToken = (token: string | null): boolean => {
  if (!token) {
    return false;
  }
  return !isTokenExpired(token);
};

/**
 * Checks if a token is about to expire (within 5 minutes)
 * @param token The JWT token to check
 * @returns True if the token is about to expire, false otherwise
 */
export const isTokenAboutToExpire = (token: string | null): boolean => {
  if (!token) {
    return true; // If no token, consider it about to expire
  }

  const payload = decodeToken(token);
  
  if (!payload || !payload.exp) {
    return true; // If there's no expiration, consider it about to expire
  }
  
  const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
  const fiveMinutes = 5 * 60; // 5 minutes in seconds
  
  return payload.exp - currentTime < fiveMinutes;
};