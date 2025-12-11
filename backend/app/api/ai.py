from fastapi import APIRouter

router = APIRouter()


# Placeholder for AI assistant endpoints (future)
@router.get("/health")
def health():
    return {"status": "healthy"}
