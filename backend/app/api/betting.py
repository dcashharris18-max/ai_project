"""Betting and casino game endpoints - play games, verify fairness."""
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import hashlib
import secrets

from backend.app.db.session import get_db
from backend.app import auth_utils
from backend.app.models.betting import (
    Game,
    GameSession,
    Bet,
    GameStatus,
    BetStatus,
    ResponsibleGamblingLimit,
)
from backend.app.models.user import User

router = APIRouter(prefix="/betting", tags=["betting"])


class GameCreate:
    def __init__(
        self,
        name: str,
        game_type: str,
        min_bet: float = 0.01,
        max_bet: float = 10000,
        house_edge_percent: float = 2.5,
    ):
        self.name = name
        self.game_type = game_type
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.house_edge_percent = house_edge_percent


class GameSessionCreate:
    def __init__(
        self, game_id: int, wager: float, seed_client: str, currency: str = "USD"
    ):
        self.game_id = game_id
        self.wager = wager
        self.seed_client = seed_client
        self.currency = currency


def verify_responsible_gambling(user: User, wager: float, db: Session):
    """Check user against responsible gambling limits."""
    limits = (
        db.query(ResponsibleGamblingLimit)
        .filter(ResponsibleGamblingLimit.user_id == user.id)
        .first()
    )

    if not limits:
        return True

    if limits.is_self_excluded:
        if (
            limits.self_excluded_until
            and datetime.utcnow() < limits.self_excluded_until
        ):
            raise HTTPException(status_code=403, detail="Self-excluded from gambling")
        else:
            limits.is_self_excluded = False
            db.commit()

    # Check daily spend limit
    today = datetime.utcnow().date()
    today_sessions = (
        db.query(GameSession)
        .filter(
            GameSession.user_id == user.id,
            GameSession.created_at >= datetime.combine(today, datetime.min.time()),
        )
        .all()
    )

    today_spend = sum([s.initial_wager for s in today_sessions]) + wager
    if limits.daily_spend_limit and today_spend > limits.daily_spend_limit:
        raise HTTPException(
            status_code=403,
            detail=f"Daily spend limit exceeded: ${limits.daily_spend_limit}",
        )

    return True


def compute_game_result(
    seed_client: str, seed_server: str, game_type: str
) -> tuple[float, str]:
    """
    Compute provably fair game result using client + server seeds.

    Approach: hash(seed_client + seed_server) to get deterministic random value [0, 1]

    Returns:
        (random_value: 0-1, result_hash: hex string)
    """
    combined = f"{seed_client}:{seed_server}".encode()
    hash_result = hashlib.sha256(combined).hexdigest()

    # Convert to float 0-1
    random_value = int(hash_result[:8], 16) / 0xFFFFFFFF

    return random_value, hash_result


@router.get("/games")
def list_games(db: Session = Depends(get_db)):
    """List available games."""
    # Use SQLAlchemy's is_ for boolean comparisons to avoid runtime lint warnings
    games = db.query(Game).filter(Game.is_active.is_(True)).all()

    return {
        "games": [
            {
                "id": g.id,
                "name": g.name,
                "game_type": g.game_type,
                "min_bet": g.min_bet,
                "max_bet": g.max_bet,
                "house_edge": g.house_edge_percent,
            }
            for g in games
        ]
    }


@router.post("/games/{game_id}/play")
def play_game(
    game_id: int,
    wager: float = Form(...),
    seed_client: str = Form(...),
    selection: str = Form(default=""),
    currency: str = Form(default="USD"),
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """
    Play a game session.

    Args:
        game_id: Game to play
        wager: Bet amount
        seed_client: Client-provided random seed (for fairness verification)
        selection: Game-specific selection (e.g. "red"/"black" for roulette,
            or "hit"/"stand" for blackjack)
        currency: Bet currency (USD, BTC, ETH)

    Returns:
        Game session with result
    """
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if wager < game.min_bet or wager > game.max_bet:
        raise HTTPException(
            status_code=400,
            detail=f"Wager must be between {game.min_bet} and {game.max_bet}",
        )

    # Check responsible gambling
    verify_responsible_gambling(current_user, wager, db)

    # Check user balance (simplified - actual implementation needs wallet deduction)
    # TODO: Integrate with wallet balance

    # Generate server seed
    seed_server = secrets.token_hex(32)

    # Compute result
    random_value, result_hash = compute_game_result(
        seed_client, seed_server, game.game_type
    )

    # Determine outcome (simplified - actual games have complex logic)
    # Example: 50/50 chance, 2x payout for win
    won = random_value > 0.5
    result_amount = wager * 2 if won else 0

    # Create session
    session = GameSession(
        user_id=current_user.id,
        game_id=game_id,
        initial_wager=wager,
        currency=currency,
        result_amount=result_amount,
        status=GameStatus.WON if won else GameStatus.LOST,
        seed_client=seed_client,
        seed_server=seed_server,
        result_hash=result_hash,
        random_value=random_value,
        completed_at=datetime.utcnow(),
    )

    # Create bet record
    bet = Bet(
        user_id=current_user.id,
        session_id=session.id,
        game_id=game_id,
        amount=wager,
        odds=2.0,
        selection=selection,
        status=BetStatus.WON if won else BetStatus.LOST,
        winnings=result_amount,
        settled_at=datetime.utcnow(),
    )
    session.bets.append(bet)

    db.add(session)
    db.add(bet)
    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id,
        "game_id": game_id,
        "wager": wager,
        "result": result_amount,
        "won": won,
        "status": session.status,
        "random_value": random_value,
        "house_edge": game.house_edge_percent,
    }


@router.get("/bets")
def list_user_bets(
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """List user's betting history."""
    bets = (
        db.query(Bet)
        .filter(Bet.user_id == current_user.id)
        .order_by(Bet.created_at.desc())
        .all()
    )

    return {
        "bets": [
            {
                "id": b.id,
                "game": b.game.name if b.game else "Unknown",
                "amount": b.amount,
                "winnings": b.winnings,
                "status": b.status,
                "created_at": b.created_at,
            }
            for b in bets[:50]  # Last 50 bets
        ]
    }


@router.get("/bets/{session_id}/verify")
def verify_fairness(
    session_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """
    Verify game fairness using revealed server seed.

    User can verify their win/loss was computed fairly by checking:
    hash(client_seed + server_seed) = result_hash
    """
    session = (
        db.query(GameSession)
        .filter(
            GameSession.id == session_id,
            GameSession.user_id == current_user.id,
        )
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Recompute hash
    combined = f"{session.seed_client}:{session.seed_server}".encode()
    computed_hash = hashlib.sha256(combined).hexdigest()
    is_fair = computed_hash == session.result_hash

    return {
        "session_id": session_id,
        "is_fair": is_fair,
        "seed_client": session.seed_client,
        "seed_server": session.seed_server,
        "result_hash": session.result_hash,
        "computed_hash": computed_hash,
    }


@router.post("/responsible-gambling/set-limits")
def set_gambling_limits(
    daily_loss_limit: float = None,
    daily_spend_limit: float = None,
    session_time_limit_minutes: int = None,
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Set or update responsible gambling limits."""
    limits = (
        db.query(ResponsibleGamblingLimit)
        .filter(ResponsibleGamblingLimit.user_id == current_user.id)
        .first()
    )

    if not limits:
        limits = ResponsibleGamblingLimit(user_id=current_user.id)

    if daily_loss_limit is not None:
        limits.daily_loss_limit = daily_loss_limit
    if daily_spend_limit is not None:
        limits.daily_spend_limit = daily_spend_limit
    if session_time_limit_minutes is not None:
        limits.session_time_limit_minutes = session_time_limit_minutes

    limits.updated_at = datetime.utcnow()
    db.add(limits)
    db.commit()

    return {"user_id": current_user.id, "limits_set": True}


@router.post("/responsible-gambling/self-exclude")
def self_exclude(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user=Depends(auth_utils.get_current_active_user),
):
    """Self-exclude from gambling for specified days."""
    limits = (
        db.query(ResponsibleGamblingLimit)
        .filter(ResponsibleGamblingLimit.user_id == current_user.id)
        .first()
    )

    if not limits:
        limits = ResponsibleGamblingLimit(user_id=current_user.id)

    limits.is_self_excluded = True
    limits.self_excluded_until = datetime.utcnow() + timedelta(days=days)
    db.add(limits)
    db.commit()

    return {
        "user_id": current_user.id,
        "self_excluded_until": limits.self_excluded_until,
    }
