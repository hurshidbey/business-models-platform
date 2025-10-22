const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
  throw new Error('Missing Supabase credentials in environment variables');
}

// Create Supabase client with service role key (bypasses RLS)
const supabase = createClient(supabaseUrl, supabaseServiceKey, {
  auth: {
    autoRefreshToken: false,
    persistSession: false
  }
});

/**
 * Create a new purchase record in the database
 */
async function createPurchase(data) {
  try {
    const { data: purchase, error } = await supabase
      .from('purchases')
      .insert([{
        email: data.email,
        stripe_payment_id: data.stripe_payment_id,
        stripe_session_id: data.stripe_session_id,
        access_token: data.access_token,
        amount_paid: data.amount_paid || 4900
      }])
      .select()
      .single();

    if (error) throw error;
    return { success: true, data: purchase };
  } catch (error) {
    console.error('Error creating purchase:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Verify access token and get purchase details
 */
async function verifyToken(token) {
  try {
    const { data, error } = await supabase
      .from('purchases')
      .select('*')
      .eq('access_token', token)
      .single();

    if (error) {
      if (error.code === 'PGRST116') {
        // No rows returned
        return { valid: false, error: 'Invalid token' };
      }
      throw error;
    }

    return { valid: true, data };
  } catch (error) {
    console.error('Error verifying token:', error);
    return { valid: false, error: error.message };
  }
}

/**
 * Update last accessed time and increment access count
 */
async function updateAccess(token, ipAddress, userAgent) {
  try {
    const { error } = await supabase
      .from('purchases')
      .update({
        last_accessed_at: new Date().toISOString(),
        access_count: supabase.rpc('increment', { row_id: token }),
        ip_address: ipAddress,
        user_agent: userAgent
      })
      .eq('access_token', token);

    if (error) throw error;
    return { success: true };
  } catch (error) {
    console.error('Error updating access:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Get all purchases (admin only)
 */
async function getAllPurchases(limit = 100, offset = 0) {
  try {
    const { data, error, count } = await supabase
      .from('purchases')
      .select('*', { count: 'exact' })
      .order('created_at', { ascending: false })
      .range(offset, offset + limit - 1);

    if (error) throw error;
    return { success: true, data, total: count };
  } catch (error) {
    console.error('Error fetching purchases:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Get purchase statistics
 */
async function getStats() {
  try {
    const { count: totalPurchases, error: countError } = await supabase
      .from('purchases')
      .select('*', { count: 'exact', head: true });

    if (countError) throw countError;

    const { data: revenueData, error: revenueError } = await supabase
      .from('purchases')
      .select('amount_paid');

    if (revenueError) throw revenueError;

    const totalRevenue = revenueData.reduce((sum, p) => sum + p.amount_paid, 0);

    // Get purchases from last 30 days
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    const { count: recentPurchases, error: recentError } = await supabase
      .from('purchases')
      .select('*', { count: 'exact', head: true })
      .gte('created_at', thirtyDaysAgo.toISOString());

    if (recentError) throw recentError;

    return {
      success: true,
      data: {
        totalPurchases,
        totalRevenue,
        averageOrderValue: totalPurchases > 0 ? totalRevenue / totalPurchases : 0,
        recentPurchases30Days: recentPurchases
      }
    };
  } catch (error) {
    console.error('Error fetching stats:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Check if email has already purchased
 */
async function checkExistingPurchase(email) {
  try {
    const { data, error } = await supabase
      .from('purchases')
      .select('access_token')
      .eq('email', email)
      .single();

    if (error) {
      if (error.code === 'PGRST116') {
        return { exists: false };
      }
      throw error;
    }

    return { exists: true, token: data.access_token };
  } catch (error) {
    console.error('Error checking existing purchase:', error);
    return { exists: false, error: error.message };
  }
}

module.exports = {
  supabase,
  createPurchase,
  verifyToken,
  updateAccess,
  getAllPurchases,
  getStats,
  checkExistingPurchase
};
