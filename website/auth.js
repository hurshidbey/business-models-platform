/**
 * Authentication & Token Verification System
 * Handles access token validation and storage
 */

const API_BASE_URL = window.location.origin + '/api';
const TOKEN_KEY = 'business_models_access_token';

/**
 * Get stored access token from localStorage
 */
function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Store access token in localStorage
 */
function setAccessToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

/**
 * Remove access token from localStorage
 */
function removeAccessToken() {
  localStorage.removeItem(TOKEN_KEY);
}

/**
 * Verify access token with backend API
 * Returns: { valid: boolean, data?: object, error?: string }
 */
async function verifyAccessToken(token) {
  try {
    const response = await fetch(`${API_BASE_URL}/verify?token=${token}`);
    const data = await response.json();

    if (response.ok && data.valid) {
      return { valid: true, data };
    } else {
      return { valid: false, error: data.error || 'Invalid token' };
    }
  } catch (error) {
    console.error('Error verifying token:', error);
    return { valid: false, error: 'Network error' };
  }
}

/**
 * Check if user has valid access
 * Redirects to homepage if no valid token
 * Call this on protected pages
 */
async function requireAuth() {
  const token = getAccessToken();

  if (!token) {
    console.log('No access token found');
    window.location.href = '/';
    return false;
  }

  // Verify token with backend
  const verification = await verifyAccessToken(token);

  if (!verification.valid) {
    console.log('Invalid access token');
    removeAccessToken();
    window.location.href = '/';
    return false;
  }

  console.log('Access granted for:', verification.data.email);
  return true;
}

/**
 * Logout user (remove token and redirect)
 */
function logout() {
  removeAccessToken();
  window.location.href = '/';
}

/**
 * Get user info from token verification
 */
async function getUserInfo() {
  const token = getAccessToken();

  if (!token) {
    return null;
  }

  const verification = await verifyAccessToken(token);

  if (verification.valid) {
    return verification.data;
  }

  return null;
}

/**
 * Display user email in UI (optional)
 */
async function displayUserEmail(elementId) {
  const userInfo = await getUserInfo();

  if (userInfo) {
    const element = document.getElementById(elementId);
    if (element) {
      element.textContent = userInfo.email;
    }
  }
}

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    getAccessToken,
    setAccessToken,
    removeAccessToken,
    verifyAccessToken,
    requireAuth,
    logout,
    getUserInfo,
    displayUserEmail
  };
}
