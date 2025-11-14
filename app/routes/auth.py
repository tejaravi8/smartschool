from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database import SessionLocal, get_db
from app.models.user import User, RoleType
from app.models.notification import Notification
from app.utils.auth_helper import (
    get_password_hash,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)
from app.utils.notification_helper import add_notification


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ------------------------- DB SESSION -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------- CURRENT USER ----------------------
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        return None

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    return user


# ------------------------- REGISTER -------------------------
@router.get("/register", response_class=HTMLResponse)
def reg_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    class_name: str = Form(None),
    roll_no: str = Form(None),
    dob: str = Form(None),
    address: str = Form(None),
    subject: str = Form(None),
    db: Session = Depends(get_db)
):

    # Admin cannot register from register page
    if role == "admin":
        return templates.TemplateResponse("register.html",
            {"request": request, "error": "Admin cannot register manually."})

    # Check if email exists
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse("register.html",
            {"request": request, "error": "Email already exists"})

    hashed = get_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed,
        role=role,
        class_name=class_name if role == "student" else None,
        roll_no=roll_no if role == "student" else None,
        dob=dob if role == "student" else None,
        address=address if role == "student" else None,
        subject=subject if role == "teacher" else None
    )

    db.add(new_user)
    db.commit()

    # 🔔 Add notification automatically
    if role == "student":
        add_notification(f"New student registered: {username}")
    elif role == "teacher":
        add_notification(f"New teacher registered: {username}")

    return RedirectResponse("/login", status_code=303)


# --------------------------- LOGIN ---------------------------
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == email, User.role == role).first()

    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse("login.html",
            {"request": request, "error": "Invalid credentials"})

    token = create_access_token({"sub": user.email, "role": user.role})
    response = RedirectResponse(f"/dashboard/{user.role.value}", status_code=303)
    response.set_cookie("access_token", token, httponly=True)

    return response


# --------------------------- LOGOUT ---------------------------
@router.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("access_token")
    return response


# ------------------------- DASHBOARDS -------------------------
@router.get("/dashboard/{role}", response_class=HTMLResponse)
def dashboard(request: Request, role: str, db: Session = Depends(get_db)):
    user = get_current_user(request)

    if not user:
        return RedirectResponse("/login")

    # prevent navigating to wrong dashboard
    if user.role.value != role:
        return RedirectResponse(f"/dashboard/{user.role.value}")

    # ---------------------- ADMIN DASHBOARD ----------------------
    if role == "admin":
        total_students = db.query(User).filter(User.role == RoleType.student).count()
        total_teachers = db.query(User).filter(User.role == RoleType.teacher).count()

        notifications = (
            db.query(Notification)
            .order_by(Notification.created_at.desc())
            .limit(5)
            .all()
        )

        return templates.TemplateResponse(
            "dashboard_admin.html",
            {
                "request": request,
                "user": user,
                "total_students": total_students,
                "total_teachers": total_teachers,
                "notifications": notifications
            }
        )

    # ------------------ STUDENT / TEACHER ------------------
    return templates.TemplateResponse(
        f"dashboard_{role}.html",
        {"request": request, "user": user}
    )


# --------------------- ADD STUDENT (ADMIN) ---------------------
@router.post("/admin/add-student")
def add_student(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    class_name: str = Form(...),
    roll_no: str = Form(...),
    dob: str = Form(...),
    address: str = Form(...),
    db: Session = Depends(get_db),
):
    hashed_pwd = get_password_hash(password)

    new_student = User(
        username=username,
        email=email,
        password=hashed_pwd,
        role="student",
        class_name=class_name,
        roll_no=roll_no,
        dob=dob,
        address=address
    )

    db.add(new_student)
    db.commit()

    add_notification(f"New student added: {username} (Class {class_name})")

    return RedirectResponse("/dashboard/admin", status_code=303)


# --------------------- ADD TEACHER (ADMIN) ---------------------
@router.post("/admin/add-teacher")
def add_teacher(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    subject: str = Form(...),
    db: Session = Depends(get_db),
):
    hashed_pwd = get_password_hash(password)

    new_teacher = User(
        username=username,
        email=email,
        password=hashed_pwd,
        role="teacher",
        subject=subject
    )

    db.add(new_teacher)
    db.commit()

    add_notification(f"New teacher added: {username} — {subject} Teacher")

    return RedirectResponse("/dashboard/admin", status_code=303)
