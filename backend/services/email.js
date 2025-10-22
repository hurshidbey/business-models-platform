const nodemailer = require('nodemailer');
require('dotenv').config();

const smtpConfig = {
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT) || 587,
  secure: false, // Use TLS
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS
  }
};

// Create reusable transporter
const transporter = nodemailer.createTransport(smtpConfig);

// Verify SMTP connection
transporter.verify(function(error, success) {
  if (error) {
    console.error('SMTP connection error:', error);
  } else {
    console.log('✓ SMTP server is ready to send emails');
  }
});

/**
 * Send access link email to customer
 */
async function sendAccessEmail(email, accessToken) {
  const accessLink = `${process.env.FRONTEND_URL}/access.html?token=${accessToken}`;

  const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      line-height: 1.6;
      color: #1a1a1a;
      background-color: #F4E8D8;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 600px;
      margin: 40px auto;
      background-color: #ffffff;
      border: 2px solid #1a1a1a;
      box-shadow: 6px 6px 0 rgba(0, 0, 0, 0.15);
    }
    .header {
      background-color: #1a1a1a;
      color: #ffffff;
      padding: 30px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 24px;
      font-weight: 600;
    }
    .content {
      padding: 40px 30px;
    }
    .content h2 {
      font-size: 20px;
      margin-top: 0;
      color: #1a1a1a;
    }
    .content p {
      font-size: 16px;
      line-height: 1.7;
      color: #2d2d2d;
      margin-bottom: 20px;
    }
    .button-container {
      text-align: center;
      margin: 35px 0;
    }
    .access-button {
      display: inline-block;
      padding: 16px 40px;
      background-color: #1a1a1a;
      color: #ffffff;
      text-decoration: none;
      font-weight: 700;
      font-size: 16px;
      border-radius: 4px;
      transition: background-color 0.3s ease;
    }
    .access-button:hover {
      background-color: #2d2d2d;
    }
    .token-box {
      background-color: #F4E8D8;
      padding: 20px;
      border: 2px solid #1a1a1a;
      border-radius: 4px;
      margin: 25px 0;
      word-break: break-all;
      font-family: monospace;
      font-size: 12px;
      color: #1a1a1a;
    }
    .features {
      margin: 30px 0;
    }
    .feature-item {
      padding: 10px 0;
      border-bottom: 1px solid #E8D5BE;
    }
    .feature-item:last-child {
      border-bottom: none;
    }
    .feature-item strong {
      color: #1a1a1a;
    }
    .footer {
      background-color: #FAF3E8;
      padding: 25px 30px;
      text-align: center;
      font-size: 14px;
      color: #2d2d2d;
      border-top: 2px solid #E8D5BE;
    }
    .footer a {
      color: #1a1a1a;
      text-decoration: none;
      font-weight: 600;
    }
    .important-note {
      background-color: #fff4e6;
      border-left: 4px solid #ff9500;
      padding: 15px;
      margin: 25px 0;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🎉 Welcome to Business Models!</h1>
    </div>

    <div class="content">
      <h2>Your Access is Ready</h2>
      <p>Thank you for your purchase! You now have lifetime access to all 60 business models with real-world examples, case studies, and implementation frameworks.</p>

      <div class="button-container">
        <a href="${accessLink}" class="access-button">Access Your Content Now →</a>
      </div>

      <div class="important-note">
        <strong>⚡ Important:</strong> Bookmark the access link above or save this email. You can use it anytime to access your content on any device.
      </div>

      <h2>What You Get:</h2>
      <div class="features">
        <div class="feature-item">
          <strong>✓ 60 Business Model Deep-Dives</strong><br>
          Comprehensive guides for every major business model
        </div>
        <div class="feature-item">
          <strong>✓ 200+ Real Company Examples</strong><br>
          Learn from Netflix, Uber, Airbnb, Tesla & more
        </div>
        <div class="feature-item">
          <strong>✓ Implementation Frameworks</strong><br>
          Step-by-step guides to apply models to your business
        </div>
        <div class="feature-item">
          <strong>✓ Case Studies</strong><br>
          Detailed analysis with financial data and insights
        </div>
        <div class="feature-item">
          <strong>✓ Lifetime Access</strong><br>
          One-time payment, access forever - no subscriptions
        </div>
        <div class="feature-item">
          <strong>✓ Regular Updates</strong><br>
          New models and examples added regularly
        </div>
      </div>

      <h2>Your Access Details:</h2>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Access Link:</strong></p>
      <div class="token-box">${accessLink}</div>

      <p>Need help? Reply to this email or contact us at <a href="mailto:support@helpingbrain.com">support@helpingbrain.com</a></p>
    </div>

    <div class="footer">
      <p><strong>Helping Brain - Business Models</strong></p>
      <p>Master business model innovation • <a href="https://helpingbrain.com">helpingbrain.com</a></p>
      <p style="margin-top: 15px; font-size: 12px; color: #666;">
        You received this email because you purchased lifetime access to our Business Models guide.
      </p>
    </div>
  </div>
</body>
</html>
  `;

  const textContent = `
Welcome to Business Models!

Your Access is Ready

Thank you for your purchase! You now have lifetime access to all 60 business models.

Access your content here:
${accessLink}

IMPORTANT: Bookmark this link or save this email. You can use it anytime to access your content on any device.

What You Get:
✓ 60 Business Model Deep-Dives
✓ 200+ Real Company Examples (Netflix, Uber, Airbnb, Tesla & more)
✓ Implementation Frameworks
✓ Case Studies with financial data
✓ Lifetime Access - no subscriptions
✓ Regular Updates

Your Access Details:
Email: ${email}
Access Link: ${accessLink}

Need help? Contact us at support@helpingbrain.com

---
Helping Brain - Business Models
https://helpingbrain.com
  `;

  try {
    const info = await transporter.sendMail({
      from: `"${process.env.FROM_NAME}" <${process.env.FROM_EMAIL}>`,
      to: email,
      subject: '🎉 Your Business Models Access is Ready!',
      text: textContent,
      html: htmlContent
    });

    console.log('✓ Email sent:', info.messageId);
    return { success: true, messageId: info.messageId };
  } catch (error) {
    console.error('Error sending email:', error);
    return { success: false, error: error.message };
  }
}

/**
 * Send admin notification email
 */
async function sendAdminNotification(purchaseData) {
  const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; }
    .container { max-width: 600px; margin: 20px auto; padding: 20px; background: #f9f9f9; border: 1px solid #ddd; }
    h2 { color: #1a1a1a; }
    .info { background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #4CAF50; }
    .label { font-weight: bold; color: #666; }
  </style>
</head>
<body>
  <div class="container">
    <h2>🎉 New Purchase!</h2>
    <div class="info">
      <p><span class="label">Email:</span> ${purchaseData.email}</p>
      <p><span class="label">Amount:</span> $${(purchaseData.amount_paid / 100).toFixed(2)}</p>
      <p><span class="label">Payment ID:</span> ${purchaseData.stripe_payment_id}</p>
      <p><span class="label">Time:</span> ${new Date().toLocaleString()}</p>
    </div>
  </div>
</body>
</html>
  `;

  try {
    const info = await transporter.sendMail({
      from: `"${process.env.FROM_NAME}" <${process.env.FROM_EMAIL}>`,
      to: process.env.FROM_EMAIL, // Send to yourself
      subject: '💰 New Business Models Purchase',
      html: htmlContent
    });

    return { success: true, messageId: info.messageId };
  } catch (error) {
    console.error('Error sending admin notification:', error);
    return { success: false, error: error.message };
  }
}

module.exports = {
  sendAccessEmail,
  sendAdminNotification
};
