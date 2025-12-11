"""Comprehensive test suite for AI Marketplace."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Tests assume these modules exist
from backend.app.main import app
from backend.app.db.session import get_db, Base


# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_db():
    """Create test database."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after test session
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    """Create fresh DB session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create test client with test database."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # Reset in-memory rate limiter between tests to avoid cross-test interference
    try:
        from backend.app import security

        security.rate_limiter.requests.clear()
    except Exception:
        pass

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client(client):
    """Create authenticated test client for use across tests."""
    client.post(
        "/auth/register",
        data={"email": "user@example.com", "password": "SecurePass123!"},
    )
    response = client.post(
        "/auth/token",
        data={"username": "user@example.com", "password": "SecurePass123!"},
    )
    token = response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}
    return client


class TestAuthEndpoints:
    """Test authentication flow."""

    def test_register_user(self, client):
        """Test user registration."""
        response = client.post(
            "/auth/register",
            data={
                "email": "test@example.com",
                "password": "SecurePass123!",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data

    def test_register_duplicate_email(self, client):
        """Test registration with existing email."""
        client.post(
            "/auth/register",
            data={"email": "test@example.com", "password": "SecurePass123!"},
        )
        response = client.post(
            "/auth/register",
            data={"email": "test@example.com", "password": "SecurePass123!"},
        )
        assert response.status_code == 400

    def test_login(self, client):
        """Test user login."""
        client.post(
            "/auth/register",
            data={"email": "test@example.com", "password": "SecurePass123!"},
        )
        response = client.post(
            "/auth/token",
            data={"username": "test@example.com", "password": "SecurePass123!"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """Test login with incorrect password."""
        client.post(
            "/auth/register",
            data={"email": "test@example.com", "password": "SecurePass123!"},
        )
        response = client.post(
            "/auth/token",
            data={"username": "test@example.com", "password": "WrongPassword1!"},
        )
        assert response.status_code == 401


class TestUserEndpoints:
    """Test user management."""


    def test_get_current_user(self, authenticated_client):
        """Test fetching current user."""
        response = authenticated_client.get("/users/me")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "user@example.com"

    def test_get_current_user_unauthorized(self, client):
        """Test unauthorized access."""
        response = client.get("/users/me")
        assert response.status_code == 401


class TestMarketplaceEndpoints:
    """Test marketplace (stores & listings)."""

    def test_create_store(self, authenticated_client):
        """Test creating a store."""
        response = authenticated_client.post(
            "/marketplace/stores",
            data={
                "name": "Tech Gadgets",
                "description": "Latest gadgets",
                "country": "US",
                "currency": "USD",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Tech Gadgets"
        assert "id" in data

    def test_create_listing(self, authenticated_client):
        """Test creating a product listing."""
        # First create store
        store_response = authenticated_client.post(
            "/marketplace/stores",
            data={"name": "Test Store", "country": "US", "currency": "USD"},
        )
        store_id = store_response.json()["id"]

        # Then create listing
        response = authenticated_client.post(
            f"/marketplace/stores/{store_id}/listings",
            data={
                "title": "Laptop",
                "description": "High-performance laptop",
                "price": "999.99",
                "currency": "USD",
                "stock": "10",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Laptop"

    def test_list_store_listings(self, authenticated_client):
        """Test listing products in store."""
        # Create store and listing
        store_response = authenticated_client.post(
            "/marketplace/stores",
            data={"name": "Test Store", "country": "US", "currency": "USD"},
        )
        store_id = store_response.json()["id"]

        authenticated_client.post(
            f"/marketplace/stores/{store_id}/listings",
            data={"title": "Laptop", "price": "999.99", "stock": "10"},
        )

        # List listings
        response = authenticated_client.get(f"/marketplace/stores/{store_id}/listings")
        assert response.status_code == 200
        data = response.json()
        assert len(data["listings"]) > 0


class TestWalletEndpoints:
    """Test wallet & transfer functionality."""

    def test_create_wallet(self, authenticated_client):
        """Test wallet creation."""
        response = authenticated_client.post(
            "/users/me/wallets",
            data={
                "currency": "BTC",
                "address": "1A1z7agoat2PYLV19cqws92pDYbV4my50q",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["currency"] == "BTC"

    def test_transfer_funds(self, authenticated_client, db_session):
        """Test user-to-user transfer."""
        # Create second user
        # For this test, we'd need another authenticated client
        # Simplified version:
        response = authenticated_client.post(
            "/wallets/transfer",
            data={
                "recipient_user_id": 2,
                "amount": "10.50",
                "currency": "USD",
            },
        )
        # Would expect status 200 or 404 depending on recipient existence
        assert response.status_code in [200, 404]


class TestSocialEndpoints:
    """Test social features."""

    def test_create_post(self, authenticated_client):
        """Test creating social post."""
        response = authenticated_client.post(
            "/social/posts",
            data={
                "content": "Just launched my new store! Check it out.",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Just launched my new store! Check it out."

    def test_feed(self, authenticated_client):
        """Test fetching social feed."""
        # Create some posts first
        authenticated_client.post("/social/posts", data={"content": "Post 1"})
        authenticated_client.post("/social/posts", data={"content": "Post 2"})

        response = authenticated_client.get("/social/feed")
        assert response.status_code == 200
        data = response.json()
        assert "posts" in data


class TestConstructionEndpoints:
    """Test construction project module."""

    def test_create_project(self, authenticated_client):
        """Test creating construction project."""
        response = authenticated_client.post(
            "/construction/projects",
            data={
                "title": "Home Renovation",
                "description": "Kitchen and bathroom remodel",
                "budget_min": "5000",
                "budget_max": "15000",
                "currency": "USD",
                "location": "New York, NY",
                "timeline_days": "90",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Home Renovation"

    def test_submit_bid(self, authenticated_client):
        """Test contractor bidding on project."""
        # Create project
        project_response = authenticated_client.post(
            "/construction/projects",
            data={
                "title": "Home Renovation",
                "budget_min": "5000",
                "budget_max": "15000",
            },
        )
        project_id = project_response.json()["id"]

        # Submit bid
        response = authenticated_client.post(
            f"/construction/projects/{project_id}/bids",
            data={
                "amount": "8000",
                "proposed_timeline_days": "60",
                "notes": "Can start immediately",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == 8000


class TestBettingEndpoints:
    """Test betting & casino module."""

    def test_list_games(self, client):
        """Test listing available games."""
        response = client.get("/betting/games")
        assert response.status_code == 200
        data = response.json()
        assert "games" in data

    def test_play_game(self, authenticated_client):
        """Test playing a game (simplified)."""
        # In real test, need to seed database with games
        response = authenticated_client.post(
            "/betting/games/1/play",
            data={
                "wager": "10.00",
                "seed_client": "abc123xyz789",
                "selection": "red",
            },
        )
        # Expect 200 if game exists, 404 if not
        assert response.status_code in [200, 404]

    def test_verify_fairness(self, authenticated_client):
        """Test fairness verification."""
        response = authenticated_client.get("/betting/bets/1/verify")
        # Expect 200 if session exists, 404 if not
        assert response.status_code in [200, 404]


class TestSecurityValidation:
    """Test input validation and security."""

    def test_email_validation(self, client):
        """Test invalid email rejection."""
        response = client.post(
            "/auth/register",
            data={"email": "invalid-email", "password": "SecurePass123!"},
        )
        assert response.status_code == 422  # Validation error

    def test_password_validation(self, client):
        """Test weak password rejection."""
        response = client.post(
            "/auth/register", data={"email": "test@example.com", "password": "weak"}
        )
        assert response.status_code == 422

    def test_sql_injection_prevention(self, client):
        """Test SQL injection prevention."""
        response = client.post(
            "/auth/token",
            data={"username": "'; DROP TABLE users; --", "password": "test"},
        )
        # Should safely reject, not execute SQL
        assert response.status_code in [401, 422]


class TestRateLimiting:
    """Test rate limiting."""

    def test_auth_rate_limit(self, client):
        """Test rate limit on login attempts."""
        # Make multiple failed login attempts
        for i in range(10):
            client.post(
                "/auth/token", data={"username": "user@test.com", "password": "wrong"}
            )

        # Should hit rate limit
        response = client.post(
            "/auth/token", data={"username": "user@test.com", "password": "wrong"}
        )
        assert response.status_code == 429  # Too Many Requests


# Integration Tests
class TestIntegrationFlows:
    """Test complete user journeys."""

    def test_marketplace_flow(self, authenticated_client):
        """Test complete marketplace flow: create store → list product → view listing."""
        # Create store
        store_response = authenticated_client.post(
            "/marketplace/stores",
            data={"name": "My Store", "country": "US", "currency": "USD"},
        )
        store_id = store_response.json()["id"]

        # Add product
        listing_response = authenticated_client.post(
            f"/marketplace/stores/{store_id}/listings",
            data={"title": "Product", "price": "99.99", "stock": "5"},
        )
        assert listing_response.status_code == 200

        # View store
        view_response = authenticated_client.get(
            f"/marketplace/stores/{store_id}/listings"
        )
        assert view_response.status_code == 200

    def test_construction_flow(self, authenticated_client):
        """Test construction project flow: create project → upload drawing → receive bid."""
        # Create project
        project_response = authenticated_client.post(
            "/construction/projects",
            data={
                "title": "Build House",
                "budget_min": "100000",
                "budget_max": "500000",
            },
        )
        project_id = project_response.json()["id"]

        # Upload drawing
        # (Simplified - real test would use file upload)

        # Bid on project
        bid_response = authenticated_client.post(
            f"/construction/projects/{project_id}/bids",
            data={"amount": "250000", "proposed_timeline_days": "180"},
        )
        # May fail if same user (can't bid own project)
        assert bid_response.status_code in [200, 400]


if __name__ == "__main__":
    # Run with: pytest backend/tests/test_api.py -v
    pytest.main([__file__, "-v", "--tb=short"])
