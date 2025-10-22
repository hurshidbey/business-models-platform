const express = require('express');
const router = express.Router();
const { verifyToken, updateAccess } = require('../services/supabase');
const { isValidTokenFormat } = require('../utils/token');

/**
 * Token Verification Endpoint
 * GET /api/verify?token=xxxxx
 *
 * Verifies if an access token is valid and returns user info
 * Also updates last_accessed_at and access_count
 */
router.get('/', async (req, res) => {
  const { token } = req.query;

  // Validate token parameter
  if (!token) {
    return res.status(400).json({
      valid: false,
      error: 'Missing token parameter'
    });
  }

  // Basic format validation
  if (!isValidTokenFormat(token)) {
    return res.status(400).json({
      valid: false,
      error: 'Invalid token format'
    });
  }

  try {
    // Verify token exists in database
    const verification = await verifyToken(token);

    if (!verification.valid) {
      return res.status(404).json({
        valid: false,
        error: 'Token not found or invalid'
      });
    }

    // Get client information
    const ipAddress = req.headers['x-forwarded-for'] ||
                     req.headers['x-real-ip'] ||
                     req.connection.remoteAddress;
    const userAgent = req.headers['user-agent'];

    // Update access tracking (non-blocking)
    updateAccess(token, ipAddress, userAgent).catch(err => {
      console.error('Failed to update access:', err);
    });

    // Return success with limited user info
    res.status(200).json({
      valid: true,
      email: verification.data.email,
      createdAt: verification.data.created_at,
      lastAccessed: verification.data.last_accessed_at
    });

  } catch (error) {
    console.error('Error verifying token:', error);
    res.status(500).json({
      valid: false,
      error: 'Server error'
    });
  }
});

/**
 * Logout Endpoint (optional - clears client-side token)
 * POST /api/verify/logout
 */
router.post('/logout', (req, res) => {
  // This is primarily handled client-side (remove from localStorage)
  // But we can log it here for analytics
  res.status(200).json({ success: true, message: 'Logged out' });
});

module.exports = router;
