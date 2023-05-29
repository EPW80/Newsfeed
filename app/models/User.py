import bcrypt
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)
    salt = Column(String(100), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.salt = bcrypt.gensalt().decode()
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), self.salt.encode("utf-8")
        ).decode()

    @validates("email")
    def validate_email(self, key, email):
        # make sure email address contains @ character
        if "@" not in email:
            raise ValueError("Invalid email address")
        return email

    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )
