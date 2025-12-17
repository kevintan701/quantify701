"""
Legal pages content for Terms of Service and Privacy Policy.
"""

TERMS_OF_SERVICE = """
# Terms of Service

**Last Updated: {date}**

## 1. Acceptance of Terms

By accessing and using Quantify 701 ("the Service"), you accept and agree to be bound by the terms and provision of this agreement.

## 2. Description of Service

Quantify 701 is a quantitative stock analysis platform that provides:
- Stock screening and ranking based on technical indicators
- AI-powered investment recommendations
- Portfolio tracking and analysis
- Trading strategy suggestions

## 3. Not Investment Advice

**IMPORTANT DISCLAIMER**: The information provided by Quantify 701 is for educational and informational purposes only. It does not constitute:
- Investment advice
- Financial planning advice
- Trading recommendations
- Solicitation to buy or sell securities

All investment decisions should be made based on your own research, risk tolerance, and financial situation. Consult with a qualified financial advisor before making investment decisions.

## 4. No Guarantees

Quantify 701 makes no guarantees about:
- The accuracy of stock data or analysis
- Investment returns or performance
- The success of any trading strategy
- Market predictions or forecasts

Past performance does not guarantee future results.

## 5. User Responsibilities

You agree to:
- Use the Service only for lawful purposes
- Not share your account credentials
- Provide accurate information when registering
- Not attempt to reverse engineer or hack the Service
- Comply with all applicable laws and regulations

## 6. Data and Privacy

Your use of the Service is also governed by our Privacy Policy. Please review it to understand how we collect and use your data.

## 7. Limitation of Liability

To the maximum extent permitted by law, Quantify 701 and The Studio 701 LLC shall not be liable for:
- Any investment losses
- Data inaccuracies
- Service interruptions
- Indirect, incidental, or consequential damages

## 8. Intellectual Property

All content, features, and functionality of the Service are owned by The Studio 701 LLC and are protected by copyright, trademark, and other intellectual property laws.

## 9. Account Termination

We reserve the right to suspend or terminate your account if you violate these Terms of Service.

## 10. Changes to Terms

We may modify these terms at any time. Continued use of the Service after changes constitutes acceptance of the new terms.

## 11. Contact

For questions about these Terms, please contact us through the app or GitHub repository.

---

**By using Quantify 701, you acknowledge that you have read, understood, and agree to be bound by these Terms of Service.**
"""

PRIVACY_POLICY = """
# Privacy Policy

**Last Updated: {date}**

## 1. Information We Collect

### Information You Provide
- Username and email address (for account creation)
- Portfolio data and preferences
- Watchlists and saved stocks
- Alert settings

### Automatically Collected Information
- Usage data and analytics
- IP address and browser information
- Session data and cookies

### Third-Party Data
- Stock market data from Yahoo Finance (public data)
- No personal financial information is collected

## 2. How We Use Your Information

We use collected information to:
- Provide and improve the Service
- Personalize your experience
- Send alerts and notifications (if enabled)
- Analyze usage patterns
- Ensure security and prevent fraud

## 3. Data Storage

- User data is stored in a secure database
- Passwords are hashed and never stored in plain text
- Data is stored on secure servers

## 4. Data Sharing

We do NOT:
- Sell your personal information
- Share data with third parties for marketing
- Disclose user data except as required by law

We may share:
- Aggregated, anonymized data for analytics
- Data with service providers (hosting, email) under strict confidentiality

## 5. Data Security

We implement:
- Password hashing (SHA-256 with salt)
- Secure database connections
- Regular security updates
- Access controls

However, no method of transmission over the internet is 100% secure.

## 6. Your Rights

You have the right to:
- Access your personal data
- Correct inaccurate data
- Delete your account and data
- Export your data
- Opt-out of non-essential communications

## 7. Cookies and Tracking

We use:
- Session cookies for authentication
- Analytics cookies (if enabled)
- No third-party advertising cookies

## 8. Children's Privacy

The Service is not intended for users under 18 years of age. We do not knowingly collect data from children.

## 9. International Users

If you are using the Service from outside the United States, you consent to the transfer of your data to the United States.

## 10. Data Retention

We retain your data:
- While your account is active
- For a reasonable period after account deletion (for backup purposes)
- As required by law

## 11. Changes to Privacy Policy

We may update this Privacy Policy. Continued use after changes constitutes acceptance.

## 12. Contact

For privacy-related questions, please contact us through the app or GitHub repository.

---

**By using Quantify 701, you acknowledge that you have read and understood this Privacy Policy.**
"""

def get_terms_of_service() -> str:
    """Get Terms of Service with current date."""
    from datetime import datetime
    return TERMS_OF_SERVICE.format(date=datetime.now().strftime("%B %d, %Y"))

def get_privacy_policy() -> str:
    """Get Privacy Policy with current date."""
    from datetime import datetime
    return PRIVACY_POLICY.format(date=datetime.now().strftime("%B %d, %Y"))

