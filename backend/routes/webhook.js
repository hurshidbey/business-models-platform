const express = require('express');
const router = express.Router();
const { verifyWebhookSignature, getCheckoutSession } = require('../services/stripe');
const { createPurchase, checkExistingPurchase } = require('../services/supabase');
const { generateAccessToken } = require('../utils/token');
const { sendAccessEmail, sendAdminNotification } = require('../services/email');

/**
 * Stripe Webhook Endpoint
 * Handles checkout.session.completed events
 *
 * IMPORTANT: This route must use raw body, not JSON parsing
 * Configure in server.js with express.raw({ type: 'application/json' })
 */
router.post('/stripe', async (req, res) => {
  const signature = req.headers['stripe-signature'];

  if (!signature) {
    console.error('Missing Stripe signature header');
    return res.status(400).json({ error: 'Missing signature' });
  }

  // Verify webhook signature
  const verification = verifyWebhookSignature(req.body, signature);

  if (!verification.valid) {
    console.error('Invalid webhook signature:', verification.error);
    return res.status(400).json({ error: 'Invalid signature' });
  }

  const event = verification.event;
  console.log('✓ Webhook received:', event.type);

  // Handle checkout.session.completed event
  if (event.type === 'checkout.session.completed') {
    try {
      const session = event.data.object;

      // Extract customer information
      const customerEmail = session.customer_details?.email || session.customer_email;
      const paymentIntentId = session.payment_intent;
      const sessionId = session.id;
      const amountTotal = session.amount_total; // Amount in cents

      if (!customerEmail) {
        console.error('No customer email in session:', sessionId);
        return res.status(400).json({ error: 'Missing customer email' });
      }

      console.log('Processing payment for:', customerEmail);

      // Check if this email already has a purchase
      const existingCheck = await checkExistingPurchase(customerEmail);

      if (existingCheck.exists) {
        console.log('Customer already has access, resending email:', customerEmail);

        // Resend access email with existing token
        await sendAccessEmail(customerEmail, existingCheck.token);

        return res.status(200).json({
          success: true,
          message: 'Access email resent',
          existing: true
        });
      }

      // Generate unique access token
      const accessToken = generateAccessToken();

      // Create purchase record in database
      const purchaseResult = await createPurchase({
        email: customerEmail,
        stripe_payment_id: paymentIntentId,
        stripe_session_id: sessionId,
        access_token: accessToken,
        amount_paid: amountTotal
      });

      if (!purchaseResult.success) {
        console.error('Failed to create purchase:', purchaseResult.error);
        return res.status(500).json({ error: 'Database error' });
      }

      console.log('✓ Purchase created:', purchaseResult.data.id);

      // Send access email to customer
      const emailResult = await sendAccessEmail(customerEmail, accessToken);

      if (!emailResult.success) {
        console.error('Failed to send email:', emailResult.error);
        // Don't fail the webhook - purchase is saved, email can be resent manually
      } else {
        console.log('✓ Access email sent to:', customerEmail);
      }

      // Send notification to admin (optional)
      await sendAdminNotification({
        email: customerEmail,
        amount_paid: amountTotal,
        stripe_payment_id: paymentIntentId
      });

      // Return success response to Stripe
      res.status(200).json({
        success: true,
        message: 'Purchase processed',
        purchaseId: purchaseResult.data.id
      });

    } catch (error) {
      console.error('Error processing webhook:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  } else {
    // Other event types (for future expansion)
    console.log('Unhandled event type:', event.type);
    res.status(200).json({ received: true });
  }
});

module.exports = router;
