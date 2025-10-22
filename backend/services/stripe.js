const Stripe = require('stripe');
require('dotenv').config();

const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

if (!stripeSecretKey) {
  throw new Error('Missing STRIPE_SECRET_KEY in environment variables');
}

const stripe = new Stripe(stripeSecretKey, {
  apiVersion: '2023-10-16'
});

/**
 * Verify Stripe webhook signature
 */
function verifyWebhookSignature(payload, signature) {
  try {
    const event = stripe.webhooks.constructEvent(
      payload,
      signature,
      webhookSecret
    );
    return { valid: true, event };
  } catch (error) {
    console.error('Webhook signature verification failed:', error.message);
    return { valid: false, error: error.message };
  }
}

/**
 * Retrieve checkout session details
 */
async function getCheckoutSession(sessionId) {
  try {
    const session = await stripe.checkout.sessions.retrieve(sessionId, {
      expand: ['customer', 'line_items']
    });
    return { success: true, session };
  } catch (error) {
    console.error('Error retrieving session:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Retrieve payment intent details
 */
async function getPaymentIntent(paymentIntentId) {
  try {
    const paymentIntent = await stripe.paymentIntents.retrieve(paymentIntentId);
    return { success: true, paymentIntent };
  } catch (error) {
    console.error('Error retrieving payment intent:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Create a refund
 */
async function createRefund(paymentIntentId, amount = null) {
  try {
    const refund = await stripe.refunds.create({
      payment_intent: paymentIntentId,
      amount: amount // Optional: partial refund
    });
    return { success: true, refund };
  } catch (error) {
    console.error('Error creating refund:', error);
    return { success: false, error: error.message };
  }
}

module.exports = {
  stripe,
  verifyWebhookSignature,
  getCheckoutSession,
  getPaymentIntent,
  createRefund
};
