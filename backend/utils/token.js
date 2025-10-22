const crypto = require('crypto');

/**
 * Generate a cryptographically secure random access token
 * @param {number} length - Length of the token (default: 64 characters)
 * @returns {string} Hex-encoded random token
 */
function generateAccessToken(length = 32) {
  return crypto.randomBytes(length).toString('hex');
}

/**
 * Hash a token using SHA-256 (optional - for storing hashed tokens)
 * @param {string} token - The token to hash
 * @returns {string} Hex-encoded hash
 */
function hashToken(token) {
  return crypto.createHash('sha256').update(token).digest('hex');
}

/**
 * Generate a short alphanumeric code (for codes, not security tokens)
 * @param {number} length - Length of the code
 * @returns {string} Random alphanumeric code
 */
function generateCode(length = 8) {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // Removed ambiguous characters
  let code = '';
  const randomBytes = crypto.randomBytes(length);

  for (let i = 0; i < length; i++) {
    code += chars[randomBytes[i] % chars.length];
  }

  return code;
}

/**
 * Verify token format (basic validation)
 * @param {string} token - Token to validate
 * @returns {boolean} True if token format is valid
 */
function isValidTokenFormat(token) {
  // Check if token is a hex string of expected length
  return typeof token === 'string' && /^[a-f0-9]{64}$/i.test(token);
}

module.exports = {
  generateAccessToken,
  hashToken,
  generateCode,
  isValidTokenFormat
};
