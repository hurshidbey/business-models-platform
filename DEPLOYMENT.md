# Deployment Guide - Business Models Platform

This guide walks you through deploying the Business Models payment-enabled platform to your Hostinger VPS.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Server Setup](#server-setup)
3. [Database Setup (Supabase)](#database-setup-supabase)
4. [Stripe Configuration](#stripe-configuration)
5. [Email Service Setup (Mailtrap)](#email-service-setup-mailtrap)
6. [Backend Deployment](#backend-deployment)
7. [Frontend Deployment](#frontend-deployment)
8. [Nginx Configuration](#nginx-configuration)
9. [SSL Certificate Setup](#ssl-certificate-setup)
10. [Testing](#testing)
11. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Prerequisites

**What you need:**
- Hostinger VPS (srv852801.hstgr.cloud / 69.62.126.73)
- Domain: helpingbrain.com (DNS pointed to VPS IP)
- SSH access (user: root, password: 20031000)
- Stripe account
- Supabase account (free tier)
- Mailtrap.io account (free tier)

**Local requirements:**
- Git installed
- SSH client (Terminal on Mac/Linux, PuTTY on Windows)

---

## Server Setup

### 1. Connect to VPS via SSH

```bash
ssh root@69.62.126.73
# Password: 20031000
```

### 2. Update System Packages

```bash
apt update && apt upgrade -y
```

### 3. Install Node.js (v18 LTS)

```bash
# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# Verify installation
node --version  # Should show v18.x.x
npm --version   # Should show 9.x.x or higher
```

### 4. Install Nginx

```bash
apt install -y nginx

# Start and enable Nginx
systemctl start nginx
systemctl enable nginx

# Verify Nginx is running
systemctl status nginx
```

### 5. Install PM2 (Process Manager)

```bash
npm install -g pm2

# Verify PM2 installation
pm2 --version
```

### 6. Install Certbot (for SSL)

```bash
apt install -y certbot python3-certbot-nginx
```

### 7. Create Directory Structure

```bash
# Create website directory
mkdir -p /var/www/helpingbrain.com

# Create backend directory
mkdir -p /var/www/helpingbrain.com/backend

# Create log directory
mkdir -p /var/www/helpingbrain.com/backend/logs

# Set proper permissions
chown -R www-data:www-data /var/www/helpingbrain.com
chmod -R 755 /var/www/helpingbrain.com
```

---

## Database Setup (Supabase)

### 1. Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up / Log in
3. Click "New Project"
4. Fill in:
   - **Project Name**: Business Models
   - **Database Password**: (save this securely)
   - **Region**: Choose closest to your VPS (e.g., US East)
5. Click "Create new project"
6. Wait 2-3 minutes for project to be ready

### 2. Get Supabase Credentials

Once project is ready:
1. Go to **Settings** → **API**
2. Copy these values:
   - **Project URL**: `https://xxxxx.supabase.co` (save as `SUPABASE_URL`)
   - **Service Role Key**: `eyJhbGc...` (save as `SUPABASE_SERVICE_KEY`)

⚠️ **Important**: Use the **service_role** key, NOT the anon key (service_role bypasses RLS)

### 3. Create Database Table

1. Go to **SQL Editor** in Supabase dashboard
2. Click "New Query"
3. Paste this SQL:

```sql
-- Create purchases table
CREATE TABLE purchases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL,
  stripe_payment_id VARCHAR(255) NOT NULL UNIQUE,
  stripe_session_id VARCHAR(255) NOT NULL UNIQUE,
  access_token VARCHAR(64) NOT NULL UNIQUE,
  amount_paid INTEGER NOT NULL DEFAULT 4900,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_accessed_at TIMESTAMP WITH TIME ZONE,
  access_count INTEGER DEFAULT 0,
  ip_address VARCHAR(45),
  user_agent TEXT
);

-- Create indexes for fast lookups
CREATE INDEX idx_purchases_email ON purchases(email);
CREATE INDEX idx_purchases_access_token ON purchases(access_token);
CREATE INDEX idx_purchases_stripe_payment_id ON purchases(stripe_payment_id);
CREATE INDEX idx_purchases_created_at ON purchases(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE purchases ENABLE ROW LEVEL SECURITY;

-- Create policy to allow service role full access
CREATE POLICY "Service role can do anything"
  ON purchases
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);
```

4. Click "Run" to execute

### 4. Verify Table Creation

1. Go to **Table Editor** in Supabase
2. You should see the `purchases` table with all columns
3. Table should be empty (0 rows)

---

## Stripe Configuration

### 1. Create Stripe Account

1. Go to [https://stripe.com](https://stripe.com)
2. Sign up / Log in
3. Activate your account (provide business details)

### 2. Get API Keys

1. Go to **Developers** → **API Keys**
2. Copy these keys:
   - **Publishable key**: `pk_test_xxxxx` (not needed for backend)
   - **Secret key**: `sk_test_xxxxx` (save as `STRIPE_SECRET_KEY`)

⚠️ Use **test mode** keys initially for testing

### 3. Create Payment Link

1. Go to **Products** → **Add Product**
2. Fill in:
   - **Name**: Business Models - Lifetime Access
   - **Description**: Access to all 60 business models and strategic frameworks
   - **Price**: $49.00 USD (one-time)
3. Click "Save product"
4. Click "Create payment link"
5. Configure:
   - **Collect customer emails**: ✅ Enabled
   - **Success URL**: `https://helpingbrain.com/checkout.html?session_id={CHECKOUT_SESSION_ID}`
   - **Cancel URL**: `https://helpingbrain.com/`
6. Click "Create link"
7. Copy the payment link URL (e.g., `https://buy.stripe.com/test_xxxxx`)
8. **Save this URL** - you'll add it to `website/index.html` later

### 4. Create Webhook Endpoint

1. Go to **Developers** → **Webhooks**
2. Click "+ Add endpoint"
3. Fill in:
   - **Endpoint URL**: `https://helpingbrain.com/api/webhook/stripe`
   - **Description**: Business Models Payment Webhook
   - **Events to send**: Select `checkout.session.completed`
4. Click "Add endpoint"
5. Click on the newly created webhook
6. Copy the **Signing secret** (starts with `whsec_...`)
7. Save as `STRIPE_WEBHOOK_SECRET`

⚠️ **Important**: Don't create the webhook until your VPS is live with SSL enabled

---

## Email Service Setup (Mailtrap)

### 1. Create Mailtrap Account

1. Go to [https://mailtrap.io](https://mailtrap.io)
2. Sign up / Log in
3. Choose **Email Sending** (not Email Testing)

### 2. Get SMTP Credentials

1. Go to **Sending Domains** → **SMTP Settings**
2. Copy these values:
   - **Host**: `live.smtp.mailtrap.io`
   - **Port**: `587`
   - **Username**: Your Mailtrap username (save as `SMTP_USER`)
   - **Password**: Your Mailtrap password (save as `SMTP_PASS`)

### 3. Verify Sending Domain (Optional but Recommended)

1. Go to **Sending Domains** → **Add Domain**
2. Enter `helpingbrain.com`
3. Add the provided DNS records to your domain registrar:
   - TXT record for SPF
   - TXT record for DKIM
   - CNAME for DKIM signature
4. Wait for verification (can take up to 48 hours)

⚠️ You can send emails without domain verification, but they may land in spam

---

## Backend Deployment

### 1. Upload Backend Code to VPS

**Option A: Using Git (Recommended)**

On your local machine:
```bash
# Make sure all backend files are committed
cd "/Users/xb21/60 Business"
git add backend/
git commit -m "Add complete backend API"
git push origin main
```

On VPS:
```bash
cd /var/www/helpingbrain.com
git clone YOUR_GITHUB_REPO_URL .
# Or if already cloned: git pull origin main
```

**Option B: Using SCP (Alternative)**

On your local machine:
```bash
scp -r "/Users/xb21/60 Business/backend" root@69.62.126.73:/var/www/helpingbrain.com/
```

### 2. Install Backend Dependencies

On VPS:
```bash
cd /var/www/helpingbrain.com/backend
npm install
```

### 3. Create Environment Variables

Create `.env` file:
```bash
cd /var/www/helpingbrain.com/backend
nano .env
```

Paste the following (replace `xxxxx` with your actual values):

```env
# Server Configuration
PORT=3001
NODE_ENV=production

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx

# Supabase Configuration
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx

# SMTP Configuration (Mailtrap)
SMTP_HOST=live.smtp.mailtrap.io
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your_mailtrap_username
SMTP_PASS=your_mailtrap_password
FROM_EMAIL=access@helpingbrain.com
FROM_NAME=Business Models

# Admin Configuration
ADMIN_PASSWORD=20031000

# CORS Configuration
CORS_ORIGIN=https://helpingbrain.com
```

Save and exit (Ctrl+O, Enter, Ctrl+X)

### 4. Secure Environment File

```bash
chmod 600 /var/www/helpingbrain.com/backend/.env
chown www-data:www-data /var/www/helpingbrain.com/backend/.env
```

### 5. Test Backend Locally

```bash
cd /var/www/helpingbrain.com/backend
npm start
```

You should see:
```
🚀 Business Models API Server
✓ Server running on port 3001
✓ Environment: production
```

Press Ctrl+C to stop

### 6. Start Backend with PM2

```bash
cd /var/www/helpingbrain.com/backend
pm2 start ecosystem.config.js

# Verify it's running
pm2 status

# View logs
pm2 logs business-models-api

# Save PM2 process list (auto-restart on reboot)
pm2 save
pm2 startup
# Follow the instructions shown
```

---

## Frontend Deployment

### 1. Upload Frontend Files to VPS

**Option A: Using Git**

On VPS:
```bash
cd /var/www/helpingbrain.com
git pull origin main
```

**Option B: Using SCP**

On your local machine:
```bash
scp -r "/Users/xb21/60 Business/website" root@69.62.126.73:/var/www/helpingbrain.com/
```

### 2. Update Stripe Payment Link in index.html

On VPS:
```bash
nano /var/www/helpingbrain.com/website/index.html
```

Find both instances of:
```html
<a href="https://buy.stripe.com/test_YOUR_PAYMENT_LINK" class="cta-button">
```

Replace `https://buy.stripe.com/test_YOUR_PAYMENT_LINK` with your actual Stripe payment link from earlier.

Save and exit (Ctrl+O, Enter, Ctrl+X)

### 3. Set Proper Permissions

```bash
chown -R www-data:www-data /var/www/helpingbrain.com/website
chmod -R 755 /var/www/helpingbrain.com/website
```

---

## Nginx Configuration

### 1. Copy Nginx Config

On VPS:
```bash
cp /var/www/helpingbrain.com/nginx/helpingbrain.com.conf /etc/nginx/sites-available/helpingbrain.com
```

### 2. Enable the Site

```bash
# Create symbolic link
ln -s /etc/nginx/sites-available/helpingbrain.com /etc/nginx/sites-enabled/

# Remove default site
rm /etc/nginx/sites-enabled/default
```

### 3. Test Nginx Configuration

```bash
nginx -t
```

Should show:
```
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 4. Reload Nginx

```bash
systemctl reload nginx
```

---

## SSL Certificate Setup

### 1. Verify DNS is Pointing to VPS

On your local machine:
```bash
dig helpingbrain.com
# Should show: 69.62.126.73
```

If not, update DNS:
1. Go to your domain registrar (Namecheap, GoDaddy, etc.)
2. Add/Update A record:
   - **Name**: `@`
   - **Type**: `A`
   - **Value**: `69.62.126.73`
   - **TTL**: `300`
3. Add CNAME for www:
   - **Name**: `www`
   - **Type**: `CNAME`
   - **Value**: `helpingbrain.com`
4. Wait 5-30 minutes for DNS propagation

### 2. Temporarily Modify Nginx Config (for initial SSL)

Since the Nginx config references SSL certificates that don't exist yet, we need to temporarily use HTTP only:

```bash
nano /etc/nginx/sites-available/helpingbrain.com
```

Comment out the HTTPS server block (add `#` at the beginning of each line from line 21 onwards).

Save and reload:
```bash
nginx -t
systemctl reload nginx
```

### 3. Obtain SSL Certificate

```bash
certbot --nginx -d helpingbrain.com -d www.helpingbrain.com
```

Follow prompts:
- Enter email: your_email@example.com
- Agree to Terms: `Y`
- Share email: `N` (optional)
- Redirect HTTP to HTTPS: `2` (Yes, redirect)

### 4. Restore Full Nginx Config

```bash
nano /etc/nginx/sites-available/helpingbrain.com
```

Uncomment the HTTPS server block (remove `#` from the lines you commented).

Save and reload:
```bash
nginx -t
systemctl reload nginx
```

### 5. Test Auto-Renewal

```bash
certbot renew --dry-run
```

Should show: "Congratulations, all renewals succeeded"

---

## Stripe Webhook Setup (Post-SSL)

Now that SSL is enabled, create the Stripe webhook:

1. Go to Stripe Dashboard → **Developers** → **Webhooks**
2. Click "+ Add endpoint"
3. Fill in:
   - **Endpoint URL**: `https://helpingbrain.com/api/webhook/stripe`
   - **Description**: Business Models Payment Webhook
   - **Events**: `checkout.session.completed`
4. Click "Add endpoint"
5. Copy the **Signing secret** (`whsec_...`)
6. Update `.env` on VPS:

```bash
nano /var/www/helpingbrain.com/backend/.env
```

Update the line:
```env
STRIPE_WEBHOOK_SECRET=whsec_YOUR_NEW_SECRET_HERE
```

Save and restart PM2:
```bash
pm2 restart business-models-api
```

---

## Testing

### 1. Test Homepage

Visit: `https://helpingbrain.com`

Should see:
- New landing page with hero section
- "Get Lifetime Access Now" button
- Features section
- FAQ section

### 2. Test Backend Health

```bash
curl https://helpingbrain.com/api/health
```

Should return:
```json
{"status":"ok","timestamp":"2025-01-15T..."}
```

### 3. Test Payment Flow (Test Mode)

1. Click "Get Lifetime Access Now" on homepage
2. Should redirect to Stripe checkout
3. Use test card: `4242 4242 4242 4242`
4. Expiry: Any future date (e.g., `12/26`)
5. CVC: Any 3 digits (e.g., `123`)
6. Enter test email: `test@example.com`
7. Click "Pay"
8. Should redirect to `/checkout.html`
9. Should see "Processing Your Payment..."
10. Within 5 seconds, should redirect to `/app/home.html`
11. Should see dashboard with your email

### 4. Check Email Delivery

1. Go to Mailtrap dashboard
2. Check "Email Logs"
3. Should see email sent to `test@example.com`
4. Subject: "Welcome to Business Models - Your Lifetime Access"

### 5. Verify Database Entry

1. Go to Supabase dashboard
2. **Table Editor** → `purchases`
3. Should see 1 row with:
   - Your test email
   - Stripe payment ID
   - Access token (64-char hex)
   - Amount: 4900 (cents = $49)

### 6. Test Access Token Verification

1. Copy the access token from Supabase
2. Visit: `https://helpingbrain.com/access.html?token=YOUR_TOKEN_HERE`
3. Should see "Access Granted!" and redirect to dashboard

### 7. Test Protected Content

1. Logout from `/app/home.html`
2. Try to visit `/app/home.html` directly
3. Should redirect to homepage (authentication required)

### 8. Switch to Live Mode (When Ready)

⚠️ Only do this when you're ready to accept real payments

1. Stripe Dashboard → Toggle "Test mode" to OFF (top right)
2. Go to **Developers** → **API Keys**
3. Copy **live** secret key (starts with `sk_live_`)
4. Go to **Webhooks** → Create new webhook with live URL
5. Copy **live** webhook secret
6. Update `.env` on VPS with live keys:

```bash
nano /var/www/helpingbrain.com/backend/.env
```

Update:
```env
STRIPE_SECRET_KEY=sk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx
```

7. Restart backend:
```bash
pm2 restart business-models-api
```

8. Create new **live** Payment Link in Stripe
9. Update `website/index.html` with new live payment link
10. Test with real card to verify

---

## Monitoring & Maintenance

### Check Backend Logs

```bash
# View real-time logs
pm2 logs business-models-api

# View log files
tail -f /var/www/helpingbrain.com/backend/logs/business-models-api-out.log
tail -f /var/www/helpingbrain.com/backend/logs/business-models-api-error.log
```

### Check Nginx Logs

```bash
# Access logs
tail -f /var/log/nginx/helpingbrain.com.access.log

# Error logs
tail -f /var/log/nginx/helpingbrain.com.error.log
```

### Monitor PM2 Process

```bash
# Process status
pm2 status

# CPU/Memory usage
pm2 monit

# Restart if needed
pm2 restart business-models-api

# Stop/Start
pm2 stop business-models-api
pm2 start business-models-api
```

### Update Application

```bash
# Pull latest changes
cd /var/www/helpingbrain.com
git pull origin main

# Restart backend
pm2 restart business-models-api

# Reload Nginx (if config changed)
nginx -t && systemctl reload nginx
```

### Backup Database

Supabase auto-backs up your database daily. To export manually:

1. Go to Supabase dashboard
2. **Database** → **Backups**
3. Click "Create backup"
4. Download when ready

### Monitor Stripe Dashboard

1. **Home** → View recent payments
2. **Payments** → Search by email/date
3. **Webhooks** → Check for failed webhook deliveries

### Renew SSL Certificate (Auto)

Certbot auto-renews. To manually renew:

```bash
certbot renew
systemctl reload nginx
```

---

## Admin Dashboard Access

Access admin dashboard at: `https://helpingbrain.com/admin` (you'll need to create this page)

Or use API directly:

```bash
# Login
curl -X POST https://helpingbrain.com/api/admin/login \
  -H "Authorization: Bearer 20031000"

# Get stats
curl https://helpingbrain.com/api/admin/stats \
  -H "Authorization: Bearer 20031000"

# Export purchases CSV
curl https://helpingbrain.com/api/admin/export \
  -H "Authorization: Bearer 20031000" > purchases.csv
```

---

## Troubleshooting

### Backend Not Starting

```bash
# Check logs
pm2 logs business-models-api

# Check .env file
cat /var/www/helpingbrain.com/backend/.env

# Test manually
cd /var/www/helpingbrain.com/backend
npm start
```

### Webhook Not Firing

1. Check Stripe Dashboard → **Developers** → **Webhooks**
2. View failed deliveries
3. Click "Send test webhook"
4. Check backend logs: `pm2 logs`

### Emails Not Sending

1. Check Mailtrap logs
2. Verify SMTP credentials in `.env`
3. Check backend logs for errors
4. Test with: `pm2 logs business-models-api | grep email`

### 502 Bad Gateway

```bash
# Check if backend is running
pm2 status

# Check Nginx error logs
tail -f /var/log/nginx/helpingbrain.com.error.log

# Restart backend
pm2 restart business-models-api
```

### Database Connection Error

1. Check Supabase URL and Service Key in `.env`
2. Verify Supabase project is running (not paused)
3. Check backend logs: `pm2 logs`

---

## Security Checklist

- [ ] `.env` file has 600 permissions
- [ ] Firewall enabled: `ufw enable` and `ufw allow 80,443/tcp`
- [ ] SSH key authentication enabled (disable password auth)
- [ ] Regular `apt update && apt upgrade`
- [ ] Stripe webhook signature verification enabled
- [ ] CORS restricted to helpingbrain.com only
- [ ] Rate limiting enabled on API endpoints
- [ ] SSL certificate auto-renewal working
- [ ] Admin password changed from default (20031000)
- [ ] Database RLS policies enabled

---

## Support

If you encounter issues:

1. Check logs (PM2, Nginx, Supabase)
2. Review this deployment guide
3. Test each component individually
4. Email support: support@helpingbrain.com

---

**Deployment Complete!** 🎉

Your Business Models platform is now live at `https://helpingbrain.com` with:
- ✅ Payment processing via Stripe
- ✅ Token-based authentication
- ✅ Email delivery via Mailtrap
- ✅ Database on Supabase
- ✅ SSL encryption
- ✅ SEO optimization
- ✅ Production-ready backend API
