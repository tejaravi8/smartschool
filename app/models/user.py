from sqlalchemy import Column, Integer, String, Enum
from enum import Enum as PyEnum
from app.database import Base

class RoleType(PyEnum):
    admin = "admin"
    teacher = "teacher"
    student = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(Enum(RoleType), default=RoleType.student, nullable=False)

    # Student fields
    class_name = Column(String(50), nullable=True)
    roll_no = Column(String(50), nullable=True)
    dob = Column(String(50), nullable=True)
    address = Column(String(200), nullable=True)

    # Teacher fields
    subject = Column(String(50), nullable=True)
