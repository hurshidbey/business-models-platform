const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// ============================================================================
// Middleware Configuration
// ============================================================================

// Security headers
app.use(helmet({
  contentSecurityPolicy: false, // Disable for now, configure later
  crossOriginEmbedderPolicy: false
}));

// CORS Configuration
const corsOptions = {
  origin: process.env.FRONTEND_URL || 'https://helpingbrain.com',
  credentials: true,
  optionsSuccessStatus: 200
};
app.use(cors(corsOptions));

// Rate Limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Max 100 requests per IP per window
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// Strict rate limit for verification endpoint
const verifyLimiter = rateLimit({
  windowMs: 1 * 60 * 1000, // 1 minute
  max: 10, // Max 10 requests per minute
  message: 'Too many verification attempts, please try again later.'
});

// ============================================================================
// Body Parsing Configuration
// ============================================================================

// IMPORTANT: Webhook endpoint needs RAW body for signature verification
// All other endpoints use JSON parsing
app.use((req, res, next) => {
  if (req.originalUrl === '/api/webhook/stripe') {
    next();
  } else {
    express.json()(req, res, next);
  }
});

// Raw body for Stripe webhook
app.use('/api/webhook/stripe', express.raw({ type: 'application/json' }));

// ============================================================================
// Routes
// ============================================================================

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Stripe webhook handler
const webhookRouter = require('./routes/webhook');
app.use('/api/webhook', webhookRouter);

// Token verification
const verifyRouter = require('./routes/verify');
app.use('/api/verify', verifyLimiter, verifyRouter);

// Admin dashboard API
const adminRouter = require('./routes/admin');
app.use('/api/admin', adminRouter);

// ============================================================================
// Error Handling
// ============================================================================

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// ============================================================================
// Server Startup
// ============================================================================

app.listen(PORT, () => {
  console.log('='.repeat(60));
  console.log('🚀 Business Models API Server');
  console.log('='.repeat(60));
  console.log(`✓ Server running on port ${PORT}`);
  console.log(`✓ Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`✓ Frontend URL: ${process.env.FRONTEND_URL}`);
  console.log('='.repeat(60));
  console.log('Endpoints:');
  console.log(`  GET  /api/health            - Health check`);
  console.log(`  POST /api/webhook/stripe    - Stripe webhook`);
  console.log(`  GET  /api/verify?token=xxx  - Verify access token`);
  console.log(`  POST /api/admin/login       - Admin authentication`);
  console.log(`  GET  /api/admin/stats       - Dashboard statistics`);
  console.log(`  GET  /api/admin/purchases   - List all purchases`);
  console.log(`  GET  /api/admin/export      - Export CSV`);
  console.log('='.repeat(60));
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  server.close(() => {
    console.log('HTTP server closed');
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT signal received: closing HTTP server');
  process.exit(0);
});

module.exports = app;
