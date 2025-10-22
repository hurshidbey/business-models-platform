const express = require('express');
const router = express.Router();
const { getAllPurchases, getStats } = require('../services/supabase');

/**
 * Simple admin authentication middleware
 * Checks for admin password in Authorization header
 */
function adminAuth(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader) {
    return res.status(401).json({ error: 'Missing authorization header' });
  }

  // Extract password from "Bearer <password>" format
  const password = authHeader.replace('Bearer ', '');

  if (password !== process.env.ADMIN_PASSWORD) {
    return res.status(403).json({ error: 'Invalid admin password' });
  }

  next();
}

/**
 * Admin Login Endpoint
 * POST /api/admin/login
 * Body: { password: "xxxxx" }
 *
 * Returns: { success: true, token: "password" } if valid
 */
router.post('/login', (req, res) => {
  const { password } = req.body;

  if (!password) {
    return res.status(400).json({ error: 'Missing password' });
  }

  if (password === process.env.ADMIN_PASSWORD) {
    res.status(200).json({
      success: true,
      token: password, // In production, use JWT
      message: 'Admin authenticated'
    });
  } else {
    res.status(403).json({ error: 'Invalid password' });
  }
});

/**
 * Get Dashboard Statistics
 * GET /api/admin/stats
 *
 * Returns: Total purchases, revenue, averages, recent activity
 */
router.get('/stats', adminAuth, async (req, res) => {
  try {
    const statsResult = await getStats();

    if (!statsResult.success) {
      return res.status(500).json({ error: statsResult.error });
    }

    res.status(200).json({
      success: true,
      stats: statsResult.data
    });

  } catch (error) {
    console.error('Error fetching stats:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

/**
 * Get All Purchases
 * GET /api/admin/purchases?limit=50&offset=0
 *
 * Returns: List of all purchases with pagination
 */
router.get('/purchases', adminAuth, async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 100;
    const offset = parseInt(req.query.offset) || 0;

    const result = await getAllPurchases(limit, offset);

    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    res.status(200).json({
      success: true,
      purchases: result.data,
      total: result.total,
      limit,
      offset
    });

  } catch (error) {
    console.error('Error fetching purchases:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

/**
 * Export Purchases to CSV
 * GET /api/admin/export
 *
 * Returns: CSV file download
 */
router.get('/export', adminAuth, async (req, res) => {
  try {
    const result = await getAllPurchases(10000, 0); // Get all

    if (!result.success) {
      return res.status(500).json({ error: result.error });
    }

    // Generate CSV
    const csvHeader = 'Email,Payment ID,Amount,Created At,Last Accessed,Access Count\n';
    const csvRows = result.data.map(p => {
      const amount = (p.amount_paid / 100).toFixed(2);
      const created = new Date(p.created_at).toLocaleString();
      const lastAccessed = p.last_accessed_at ? new Date(p.last_accessed_at).toLocaleString() : 'Never';

      return `"${p.email}","${p.stripe_payment_id}","$${amount}","${created}","${lastAccessed}",${p.access_count}`;
    }).join('\n');

    const csv = csvHeader + csvRows;

    // Set headers for file download
    res.setHeader('Content-Type', 'text/csv');
    res.setHeader('Content-Disposition', 'attachment; filename="purchases.csv"');
    res.status(200).send(csv);

  } catch (error) {
    console.error('Error exporting purchases:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

/**
 * Search Purchases by Email
 * GET /api/admin/search?email=user@example.com
 */
router.get('/search', adminAuth, async (req, res) => {
  try {
    const { email } = req.query;

    if (!email) {
      return res.status(400).json({ error: 'Missing email parameter' });
    }

    const { supabase } = require('../services/supabase');

    const { data, error } = await supabase
      .from('purchases')
      .select('*')
      .ilike('email', `%${email}%`)
      .order('created_at', { ascending: false });

    if (error) throw error;

    res.status(200).json({
      success: true,
      results: data,
      count: data.length
    });

  } catch (error) {
    console.error('Error searching purchases:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
