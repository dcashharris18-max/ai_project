# Testing Guide

## Overview

Complete testing strategy for the AI Marketplace platform, covering unit tests, integration tests, and end-to-end tests.

## Quick Start

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Run all tests
pytest backend/tests -v

# Run with coverage report
pytest backend/tests --cov=backend/app --cov-report=html

# Run specific test file
pytest backend/tests/test_api.py::TestAuthEndpoints -v

# Run tests matching pattern
pytest -k "test_login" -v
```

## Test Structure

```
backend/tests/
├── test_api.py              # API endpoint tests
├── test_models.py           # Database model tests
├── test_security.py         # Security & validation tests
├── conftest.py              # Shared fixtures
└── fixtures/
    ├── user_fixtures.py     # User test data
    ├── wallet_fixtures.py   # Wallet test data
    └── marketplace_fixtures.py
```

## 1. Unit Tests

### Database Models

```python
# backend/tests/test_models.py
import pytest
from app.models.user import User
from app.models.wallet import Wallet

class TestUserModel:
    """Test User model."""
    
    def test_user_creation(self, db_session):
        """Test creating user."""
        user = User(
            email="test@example.com",
            hashed_password="hash_here",
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
    
    def test_user_kyc_fields(self, db_session):
        """Test KYC field storage."""
        user = User(
            email="kyc@example.com",
            hashed_password="hash",
            first_name="John",
            last_name="Doe",
            country="US",
            kyc_status="pending",
        )
        db_session.add(user)
        db_session.commit()
        
        retrieved = db_session.query(User).filter_by(email="kyc@example.com").first()
        assert retrieved.first_name == "John"
        assert retrieved.kyc_status == "pending"


class TestWalletModel:
    """Test Wallet model."""
    
    def test_wallet_creation(self, db_session, user):
        """Test creating wallet for user."""
        wallet = Wallet(
            user_id=user.id,
            address="0x742d35Cc6634C0532925a3b844Bc9e7595f42bE",
            currency="ETH",
            balance=10.5,
        )
        db_session.add(wallet)
        db_session.commit()
        
        assert wallet.id is not None
        assert wallet.user_id == user.id
        assert wallet.balance == 10.5
```

### CRUD Operations

```python
# backend/tests/test_crud.py
import pytest
from app import crud
from app.schemas import UserCreate

class TestUserCRUD:
    """Test User CRUD operations."""
    
    def test_create_user(self, db_session):
        """Test user creation via CRUD."""
        user_in = UserCreate(
            email="crud@example.com",
            password="SecurePass123!",
        )
        user = crud.create_user(db_session, user_in)
        
        assert user.email == "crud@example.com"
        assert user.id is not None
    
    def test_get_user_by_email(self, db_session, user):
        """Test retrieving user by email."""
        retrieved = crud.get_user_by_email(db_session, user.email)
        
        assert retrieved.id == user.id
        assert retrieved.email == user.email
    
    def test_update_user_kyc(self, db_session, user):
        """Test KYC update."""
        update_data = {
            "kyc_status": "verified",
            "country": "US",
        }
        updated = crud.update_user_kyc(db_session, user.id, update_data)
        
        assert updated.kyc_status == "verified"
```

## 2. Integration Tests

### Authentication Flow

```python
# backend/tests/test_auth_integration.py
import pytest

class TestAuthenticationFlow:
    """Test complete authentication flow."""
    
    def test_register_and_login(self, client):
        """Test registration followed by login."""
        # Register
        reg_response = client.post(
            "/auth/register",
            data={
                "email": "flow@example.com",
                "password": "SecurePass123!",
            }
        )
        assert reg_response.status_code == 200
        user_id = reg_response.json()["id"]
        
        # Login
        login_response = client.post(
            "/auth/token",
            data={
                "username": "flow@example.com",
                "password": "SecurePass123!",
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Access protected endpoint
        client.headers = {"Authorization": f"Bearer {token}"}
        protected_response = client.get("/users/me")
        assert protected_response.status_code == 200
        assert protected_response.json()["id"] == user_id
```

### Marketplace Flow

```python
class TestMarketplaceFlow:
    """Test complete marketplace workflow."""
    
    def test_store_creation_and_listing(self, authenticated_client):
        """Test creating store and adding products."""
        # Create store
        store_response = authenticated_client.post(
            "/marketplace/stores",
            data={
                "name": "Tech Store",
                "description": "Latest gadgets",
                "country": "US",
                "currency": "USD",
            }
        )
        assert store_response.status_code == 200
        store_id = store_response.json()["id"]
        
        # Add product
        product_response = authenticated_client.post(
            f"/marketplace/stores/{store_id}/listings",
            data={
                "title": "Laptop",
                "description": "High-end laptop",
                "price": "1299.99",
                "currency": "USD",
                "stock": "5",
            }
        )
        assert product_response.status_code == 200
        
        # View products in store
        list_response = authenticated_client.get(
            f"/marketplace/stores/{store_id}/listings"
        )
        assert list_response.status_code == 200
        listings = list_response.json()["listings"]
        assert len(listings) > 0
        assert listings[0]["title"] == "Laptop"
```

## 3. API Endpoint Tests

### Request/Response Validation

```python
class TestMarketplaceValidation:
    """Test API input validation."""
    
    def test_invalid_price(self, authenticated_client):
        """Test invalid product price."""
        # Create store first
        store_response = authenticated_client.post(
            "/marketplace/stores",
            data={"name": "Store", "country": "US", "currency": "USD"}
        )
        store_id = store_response.json()["id"]
        
        # Try invalid price
        response = authenticated_client.post(
            f"/marketplace/stores/{store_id}/listings",
            data={
                "title": "Product",
                "price": "invalid",  # Should fail
                "stock": "10",
            }
        )
        assert response.status_code in [400, 422]  # Validation error
    
    def test_missing_required_field(self, authenticated_client):
        """Test missing required field."""
        response = authenticated_client.post(
            "/marketplace/stores",
            data={"name": "Store"}  # Missing 'country'
        )
        assert response.status_code == 422
```

## 4. Security Tests

### Input Validation

```python
# backend/tests/test_security.py
class TestInputValidation:
    """Test security input validation."""
    
    def test_sql_injection_prevention(self, client):
        """Test SQL injection prevention."""
        response = client.post(
            "/auth/token",
            data={
                "username": "'; DROP TABLE users; --",
                "password": "test",
            }
        )
        # Should fail safely, not crash
        assert response.status_code in [401, 422]
        assert "DROP TABLE" not in response.text
    
    def test_xss_prevention(self, authenticated_client):
        """Test XSS payload handling."""
        response = authenticated_client.post(
            "/social/posts",
            data={
                "content": "<script>alert('xss')</script>",
            }
        )
        assert response.status_code == 200
        # Should be escaped
        post = response.json()
        assert "<script>" not in post["content"]
    
    def test_email_validation(self, client):
        """Test email format validation."""
        response = client.post(
            "/auth/register",
            data={
                "email": "not-an-email",
                "password": "SecurePass123!",
            }
        )
        assert response.status_code == 422
```

### Rate Limiting

```python
class TestRateLimiting:
    """Test rate limiting."""
    
    def test_auth_rate_limit(self, client):
        """Test rate limit on login endpoint."""
        # Make 6 requests (limit is 5/min)
        for i in range(6):
            response = client.post(
                "/auth/token",
                data={"username": "user", "password": "wrong"},
            )
        
        # 6th should be rate limited
        assert response.status_code == 429
```

## 5. Fixture Management

### Conftest (Shared Fixtures)

```python
# backend/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db, Base
from app import crud
from app.schemas import UserCreate

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session")
def db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db):
    """Provide database session for test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Provide test client."""
    return TestClient(app)


@pytest.fixture
def user(db_session):
    """Create test user."""
    user_in = UserCreate(
        email="test@example.com",
        password="TestPass123!",
    )
    return crud.create_user(db_session, user_in)


@pytest.fixture
def authenticated_client(client, user):
    """Provide authenticated test client."""
    response = client.post(
        "/auth/token",
        data={
            "username": user.email,
            "password": "TestPass123!",
        }
    )
    token = response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}
    return client
```

## 6. Performance Tests

### Load Testing with Locust

```bash
pip install locust
```

```python
# backend/tests/locustfile.py
from locust import HttpUser, task, between

class APIUser(HttpUser):
    """Simulate API user behavior."""
    
    wait_time = between(1, 3)
    token = None
    
    @task(1)
    def register(self):
        """Register new user."""
        self.client.post(
            "/auth/register",
            data={
                "email": f"user{random.randint(0, 10000)}@example.com",
                "password": "SecurePass123!",
            }
        )
    
    @task(5)
    def get_feed(self):
        """Get social feed."""
        self.client.get("/social/feed")
    
    @task(2)
    def list_stores(self):
        """List marketplace stores."""
        self.client.get("/marketplace/stores")
```

Run: `locust -f backend/tests/locustfile.py -u 100 -r 10 -t 5m http://localhost:8000`

## 7. Coverage Reports

```bash
# Generate coverage report
pytest backend/tests --cov=backend/app --cov-report=html

# View report
open htmlcov/index.html

# Show coverage by file
pytest backend/tests --cov=backend/app --cov-report=term-missing
```

### Coverage Goals
- Overall: >80%
- Critical modules (auth, payments): >95%
- Models, CRUD: >90%
- API routes: >85%

## 8. Continuous Integration

### GitHub Actions

```yaml
# .github/workflows/ci-cd.yml
- name: Run tests
  run: |
    pytest backend/tests \
      -v \
      --cov=backend/app \
      --cov-report=xml
```

### Pre-commit Hook

```bash
# Create .git/hooks/pre-commit
#!/bin/bash
pytest backend/tests -q || exit 1
```

## 9. Test Data Management

### Factories for Test Objects

```python
# backend/tests/factories.py
from factory import Factory, Sequence
from app.models.user import User

class UserFactory(Factory):
    """Factory for creating test users."""
    
    class Meta:
        model = User
    
    email = Sequence(lambda n: f"user{n}@example.com")
    hashed_password = "hash_here"
    is_active = True

# Usage:
user = UserFactory.create()
users = UserFactory.create_batch(10)
```

## 10. Test Best Practices

- **Isolation**: Each test should be independent
- **Clarity**: Test names should describe what's tested
- **Setup/Teardown**: Use fixtures for common setup
- **Assertions**: Use clear, specific assertions
- **Mocking**: Mock external services (Stripe, CCXT)
- **Speed**: Unit tests <1s, integration <5s
- **Documentation**: Comment on why test exists, not what it does

### Example Best Practice

```python
# Good test
def test_transfer_creates_ailog_entry(authenticated_client, recipient_user):
    """Verify transfer operation creates activity log for both users."""
    # Setup: Get initial log count
    initial_logs = authenticated_client.get("/ai/logs").json()["logs"]
    initial_count = len(initial_logs)
    
    # Action: Transfer funds
    authenticated_client.post(
        "/wallets/transfer",
        data={
            "recipient_user_id": recipient_user.id,
            "amount": "50.00",
            "currency": "USD",
        }
    )
    
    # Assert: Verify log was created
    new_logs = authenticated_client.get("/ai/logs").json()["logs"]
    assert len(new_logs) == initial_count + 1
    assert new_logs[0]["message"].startswith("Sent")
```

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/faq/testing.html)
- [Locust Load Testing](https://locust.io/)
