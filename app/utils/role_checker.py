from fastapi import Request
from fastapi.responses import RedirectResponse
from app.utils.current_user import get_current_user

def role_required(request: Request, allowed_roles: list):
    user = get_current_user(request)

    # If no user found → back to login
    if not user:
        return RedirectResponse("/login", status_code=303)

    # If user role not allowed → redirect to their own dashboard
    if user.role.value not in allowed_roles:
        return RedirectResponse(f"/dashboard/{user.role.value}", status_code=303)

    return user
