from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.database import Base, engine, SessionLocal
from app.models.user import User, RoleType
from app.routes import auth
from app.utils.auth_helper import get_password_hash


app = FastAPI()
app.include_router(auth.router)

templates = Jinja2Templates(directory="app/templates")

# Create all tables
Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# Auto create admin if not exists
def create_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.role == RoleType.admin).first()

    if not admin:
        default_admin = User(
            username="SuperAdmin",
            email="admin@school.com",
            password=get_password_hash("admin123"),
            role=RoleType.admin,
        )
        db.add(default_admin)
        db.commit()
        print("✅ Default admin created: admin@school.com / admin123")
    else:
        print("ℹ Admin exists already")

    db.close()


create_admin()
