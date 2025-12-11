# Security Hardening Guide

## Overview

This document covers production-grade security implementations for the AI Marketplace platform.

## 1. Authentication & Authorization

### JWT Best Practices
- **Token Expiry**: 15-60 minutes for access tokens, 24 hours for refresh tokens
- **Signing Algorithm**: HS256 (HMAC-SHA256) or RS256 (RSA)
- **Secret Key**: Minimum 32 bytes, stored in environment variables (never in code)

```python
# Example from auth_utils.py
TOKEN_EXPIRE_MINUTES = 60
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
```

### Password Security
- **Minimum 8 characters** with letter + digit + special character
- **Bcrypt hashing** with work factor ≥ 12
- **No plaintext storage** - never log or display passwords

### Role-Based Access Control (RBAC)
```python
# Models support: user, contractor, store_owner, admin
# Add roles column to User model:
role = Column(String, default="user")  # user, contractor, store_owner, admin
```

## 2. Network Security

### CORS Configuration
```python
# Restrict to known frontend origins
ALLOWED_ORIGINS = [
    "https://app.example.com",
    "https://dashboard.example.com",
]

# Only allow specific HTTP methods
allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
```

### HTTPS Enforcement
- **Certificate**: Use Let's Encrypt or paid SSL provider
- **HSTS**: Force HTTPS with `Strict-Transport-Security: max-age=31536000`
- **Redirect HTTP to HTTPS**: All HTTP requests → 301 redirect to HTTPS

### Security Headers
```
X-Frame-Options: DENY  # Prevent clickjacking
X-Content-Type-Options: nosniff  # Prevent MIME sniffing
Content-Security-Policy: default-src 'self'  # XSS protection
X-XSS-Protection: 1; mode=block  # Legacy XSS filter
```

## 3. Input Validation & Sanitization

### Validation Rules
```python
from app.security import InputValidator

# Email
validator.validate_email(email)  # Check format, max 254 chars

# Password
validator.validate_password(pwd)  # Check strength, max 512 chars

# General strings
validator.validate_string(value)  # Max 2000 chars, non-empty

# File uploads
max_size_mb = 50
secure_filename = validator.sanitize_filename(filename)
```

### SQL Injection Prevention
- **Always use parameterized queries** (SQLAlchemy ORM does this)
- **Never concatenate user input into SQL strings**

Example ✅ Safe:
```python
user = db.query(User).filter(User.email == email).first()
```

Example ❌ Unsafe:
```python
user = db.execute(f"SELECT * FROM user WHERE email = '{email}'")
```

### XSS Prevention
- React automatically escapes content in JSX
- For HTML content, use `dangerouslySetInnerHTML` only with sanitized content
- Use library: `npm install dompurify` for HTML sanitization

## 4. Rate Limiting

### Implementation
```python
from app.security import rate_limiter

# Per IP, per endpoint
rate_limiter.is_allowed(ip, endpoint, limit=5, window_seconds=60)
```

### Recommended Limits
- **Auth endpoints** (login, register): 5 requests/minute/IP
- **General API**: 100 requests/minute/IP
- **File uploads**: 10 requests/minute/user
- **Trading endpoints**: 30 requests/minute/user

## 5. Secrets Management

### Environment Variables
**Production must use:**
- AWS Secrets Manager
- HashiCorp Vault
- Google Secret Manager
- Azure Key Vault

**Never commit:**
- `.env` files to GitHub
- API keys or passwords in code
- Database credentials in configuration

### .env.example (Safe to commit)
```
DATABASE_URL=postgresql://user:password@localhost/db
SECRET_KEY=your-secret-key-here
STRIPE_API_KEY=sk_test_...
CCXT_API_KEYS={"exchange": "key", ...}
```

## 6. Database Security

### PostgreSQL Hardening
```sql
-- Create limited-privilege user for app
CREATE USER app_user WITH PASSWORD 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

-- Disable superuser on app account
ALTER ROLE app_user NOSUPERUSER;

-- Enable SSL
ssl = on
ssl_cert_file = '/path/to/cert.pem'
ssl_key_file = '/path/to/key.pem'
```

### Connection Pooling
```python
# Use connection pooling to prevent exhaustion
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,  # Test connections before use
)
```

## 7. File Upload Security

### Safe File Handling
```python
# backend/app/api/marketplace.py
import os
from pathlib import Path

UPLOAD_DIR = Path("backend/storage/product_images")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Validate
if file.size > MAX_FILE_SIZE:
    raise HTTPException(status_code=413, detail="File too large")

if Path(file.filename).suffix.lower() not in ALLOWED_EXTENSIONS:
    raise HTTPException(status_code=400, detail="Invalid file type")

# Save with sanitized name
safe_name = security.InputValidator.sanitize_filename(file.filename)
filepath = UPLOAD_DIR / f"{user_id}_{datetime.utcnow().timestamp()}_{safe_name}"
```

## 8. Blockchain & Wallet Security

### Non-Custodial Wallets
```python
# backend/app/services/wallet_manager.py

# Generate HD wallet from mnemonic
from mnemonic import Mnemonic
m = Mnemonic('english')
mnemonic = m.generate(strength=128)  # 12-word

# Encrypt private keys
from cryptography.fernet import Fernet
f = Fernet(encryption_key)
encrypted_key = f.encrypt(private_key_bytes)
```

### RPC Provider Security
- Use **HTTPS only** endpoints
- Never embed RPC URLs in frontend (use backend proxy)
- Implement **request signing** for transaction submission
- Keep **nonce tracking** to prevent replay attacks

## 9. API Logging & Monitoring

### Structured Logging
```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Log with context (never passwords)
logger.info(
    "User login attempt",
    extra={
        "user_id": user_id,
        "ip": request.client.host,
        "success": True
    }
)
```

### Monitoring Checklist
- Failed login attempts (alert after 5 in 1 minute)
- Large withdrawals (alert on >$10k)
- Unusual API usage (alert on spike >200% baseline)
- Database errors and slow queries (>1s)
- Disk space warnings (<10% free)
- Certificate expiration (alert 30 days before)

## 10. Compliance & Legal

### Data Privacy (GDPR/CCPA)
- **Consent**: Collect before storing user data
- **Right to erasure**: Implement user data deletion endpoint
- **Data portability**: Export user data in standard format
- **Privacy policy**: Clear, accessible privacy page

### KYC/AML Requirements (if handling currency)
- **Verify identity**: Government ID check
- **Address verification**: Proof of address
- **Sanctions checking**: Screen against government lists
- **PEP screening**: Check for politically exposed persons
- **Record keeping**: Maintain KYC records for 5-7 years

### Responsible Gambling (Betting Module)
- **Geolocation restrictions**: Disable gambling in prohibited regions
- **Age verification**: Confirm user is 18+
- **Self-exclusion**: Implement self-exclusion periods
- **Loss limits**: Allow users to set daily/weekly loss limits
- **Problem gambling resources**: Display helpline numbers

## 11. Dependency Management

### Regular Updates
```bash
# Check for vulnerabilities
pip-audit
safety check

# Update dependencies safely
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --upgrade --dry-run
pip install -r requirements.txt --upgrade
```

### Lock Dependencies
```bash
# Use requirements.txt with pinned versions
pip freeze > requirements.lock
```

## 12. Testing Security

### Test Coverage
```bash
pytest --cov=backend/app --cov-report=html
# Aim for >80% coverage
```

### Security-Specific Tests
```python
# test_security.py
def test_sql_injection_prevention():
    """Ensure SQL injection attempts are safely rejected."""
    response = client.post("/auth/token", data={
        "username": "'; DROP TABLE users; --",
        "password": "test"
    })
    assert response.status_code != 500  # Don't crash

def test_xss_prevention():
    """Ensure XSS payloads are escaped."""
    response = client.post("/social/posts", data={
        "content": "<script>alert('xss')</script>"
    })
    assert "<script>" not in response.text

def test_rate_limiting():
    """Ensure rate limits are enforced."""
    for i in range(10):
        client.post("/auth/token", data={"username": "x", "password": "x"})
    response = client.post("/auth/token", data={"username": "x", "password": "x"})
    assert response.status_code == 429
```

## 13. Incident Response Plan

### Security Incident Flowchart
```
1. Detect (monitoring alerts)
   ↓
2. Isolate (take affected service offline if needed)
   ↓
3. Investigate (review logs, check for data loss)
   ↓
4. Remediate (patch vulnerability, rotate credentials)
   ↓
5. Notify (inform affected users if data exposed)
   ↓
6. Document (post-mortem, lessons learned)
```

### Key Contacts
- Security Team Lead: security@example.com
- Incident On-Call: +1-555-0100
- Legal Team: legal@example.com

## 14. Production Deployment Checklist

- [ ] SSL/TLS certificate installed
- [ ] HTTPS enforced (HTTP → redirect)
- [ ] CORS configured for production origin
- [ ] Rate limiting enabled
- [ ] Database backups configured (hourly)
- [ ] WAF (Web Application Firewall) deployed
- [ ] DDoS protection enabled
- [ ] Monitoring & alerting active
- [ ] API keys rotated
- [ ] Secrets in environment variables
- [ ] `.env` files NOT in git
- [ ] Database encryption at rest
- [ ] Logs centralized (CloudWatch, Splunk, etc)
- [ ] Documentation updated
- [ ] Security headers verified
- [ ] Dependencies up-to-date
- [ ] Tests passing (>80% coverage)
- [ ] Code reviewed by security team

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/2023/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/sql-syntax.html)
