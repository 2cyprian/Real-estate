from fastapi import APIRouter, Depends
from app.users.models import User
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Returns the currently authenticated user's basic info.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name if hasattr(current_user, "first_name") else None,
        "last_name": current_user.last_name if hasattr(current_user, "last_name") else None,
    }
