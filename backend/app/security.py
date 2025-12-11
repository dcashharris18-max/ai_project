"""Security hardening middleware and utilities."""
from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
try:
    from starlette.middleware.gzip import GZIPMiddleware
except Exception:
    GZIPMiddleware = None
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)


def setup_security_middleware(app):
    """Configure all security middleware."""

    # CORS - restrict to frontend origins
    allowed_origins = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000"
    ).split(",")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted Host - prevent Host header attacks
    # Build a proper allowed hosts list (TrustedHost expects hostnames, not full URLs)
    from urllib.parse import urlparse

    allowed_hosts_env = os.getenv("ALLOWED_HOSTS")
    if allowed_hosts_env:
        allowed_hosts = [h.strip() for h in allowed_hosts_env.split(",") if h.strip()]
    else:
        hosts = []
        for o in allowed_origins:
            try:
                parsed = urlparse(o)
                host = parsed.hostname or o
                hosts.append(host)
            except Exception:
                hosts.append(o)
        # include common local/test hosts
        allowed_hosts = list(dict.fromkeys(hosts + ["localhost", "127.0.0.1", "testserver"]))

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

    # Compression (optional depending on starlette version)
    if GZIPMiddleware is not None:
        app.add_middleware(GZIPMiddleware, minimum_size=1000)


def setup_security_headers(app):
    """Add security headers to responses."""

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Prevent MIME sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Enable XSS protection (legacy, modern browsers use CSP)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' https:; "
        )

        # HSTS - force HTTPS
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000; includeSubDomains"

        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy
        response.headers[
            "Permissions-Policy"
        ] = "geolocation=(), microphone=(), camera=(), payment=()"

        return response


def setup_request_logging(app):
    """Log all requests with sanitization."""

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        # Don't log passwords/sensitive data
        path = request.url.path
        method = request.method

        # Sanitize sensitive paths
        sensitive_paths = ["/auth", "/kyc", "/wallet"]
        sanitized_path = (
            path if not any(p in path for p in sensitive_paths) else path.split("?")[0]
        )

        start_time = datetime.utcnow()
        response = await call_next(request)
        duration = (datetime.utcnow() - start_time).total_seconds()

        logger.info(
            f"{method} {sanitized_path} - {response.status_code} - {duration:.3f}s",
            extra={"user_agent": request.headers.get("user-agent", "unknown")},
        )

        return response


class InputValidator:
    """Input validation utilities."""

    MAX_STRING_LENGTH = 2000
    MAX_EMAIL_LENGTH = 254
    MAX_PASSWORD_LENGTH = 512
    MIN_PASSWORD_LENGTH = 8
    MAX_FILE_SIZE_MB = 50

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        if not email or len(email) > InputValidator.MAX_EMAIL_LENGTH:
            return False
        # Basic regex
        return "@" in email and "." in email.split("@")[1]

    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate password strength."""
        if not password or len(password) < InputValidator.MIN_PASSWORD_LENGTH:
            return False
        if len(password) > InputValidator.MAX_PASSWORD_LENGTH:
            return False

        # Must have letter, number, and special char
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        return has_letter and has_digit and has_special

    @staticmethod
    def validate_string(value: str, max_length: int = None) -> bool:
        """Validate string input."""
        if not isinstance(value, str):
            return False
        if len(value) == 0:
            return False
        max_len = max_length or InputValidator.MAX_STRING_LENGTH
        if len(value) > max_len:
            return False
        return True

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Remove dangerous characters from filename."""
        import re

        # Allow alphanumeric, dash, underscore, dot
        sanitized = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)
        return sanitized[:255]  # Limit length


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self):
        self.requests = {}  # {ip: [(timestamp, endpoint), ...]}

    def is_allowed(
        self, ip: str, endpoint: str, limit: int = 100, window_seconds: int = 60
    ) -> bool:
        """Check if request is within rate limit."""
        now = datetime.utcnow().timestamp()
        key = f"{ip}:{endpoint}"

        if key not in self.requests:
            self.requests[key] = []

        # Remove old entries outside window
        self.requests[key] = [
            (ts, ep) for ts, ep in self.requests[key] if now - ts < window_seconds
        ]

        # Check limit
        if len(self.requests[key]) >= limit:
            return False

        # Add new request
        self.requests[key].append((now, endpoint))
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


def setup_rate_limiting(app):
    """Setup rate limiting middleware."""

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        # Bypass only when explicit TESTING env var set; keep limiter active for TestClient
        if os.getenv("TESTING"):
            return await call_next(request)

        ip = request.client.host if request.client else "unknown"
        endpoint = request.url.path

        # Strict limits on auth endpoints (5/min)
        if endpoint in ["/auth/login", "/auth/register", "/auth/token"]:
            if not rate_limiter.is_allowed(ip, endpoint, limit=5, window_seconds=60):
                return Response(
                    content='{"detail": "Too many requests. Try again later."}',
                    status_code=429,
                    media_type="application/json",
                )

        # General limit (100/min)
        elif not rate_limiter.is_allowed(ip, "general", limit=100, window_seconds=60):
            return Response(
                content='{"detail": "Rate limit exceeded."}',
                status_code=429,
                media_type="application/json",
            )

        return await call_next(request)


def setup_error_handlers(app):
    """Setup error handlers with sanitization."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """Sanitize validation error messages."""
        # Don't expose internal details in production
        logger.warning(f"Validation error on {request.url.path}: {exc}")

        return Response(
            content='{"detail": "Invalid request"}',
            status_code=422,
            media_type="application/json",
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected errors."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)

        # Don't expose stack traces in production
        return Response(
            content='{"detail": "Internal server error"}',
            status_code=500,
            media_type="application/json",
        )
