from fastapi import FastAPI
from backend.app.api import auth, users
from backend.app.api import (
    marketplace,
    social,
    orders,
    wallets,
    ai,
    construction,
    betting,
)
from backend.app.db.session import engine, Base
from backend.app import security
from backend.app import models  # ensure model modules are imported and registered

app = FastAPI(
    title="AI Marketplace Backend",
    description="Complete crypto marketplace with trading, social, construction, and betting",
    version="1.0.0",
)

# Apply security hardening
security.setup_security_middleware(app)
security.setup_security_headers(app)
security.setup_request_logging(app)
security.setup_rate_limiting(app)
security.setup_error_handlers(app)

# Register API routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(marketplace.router, prefix="/marketplace", tags=["marketplace"])
app.include_router(social.router, prefix="/social", tags=["social"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(wallets.router, prefix="/wallets", tags=["wallets"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(construction.router)
app.include_router(betting.router)


@app.on_event("startup")
def on_startup():
    # Create tables (simple approach for development)
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "AI Marketplace API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
