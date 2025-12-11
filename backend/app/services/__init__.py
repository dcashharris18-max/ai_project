try:
	from backend.app.services import trading, payments
except Exception:
	# Allow importing the services package even if optional heavy deps
	# (ccxt, stripe, etc.) are not installed in constrained environments.
	trading = None
	payments = None

__all__ = ["trading", "payments"]
