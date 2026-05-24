import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from passlib.context import CryptContext
from jose import JWTError, jwt
from database import db

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24  # 30 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, email: str, role: str) -> str:
    """Create JWT access token"""
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    
    to_encode = {
        "sub": user_id,
        "email": email,
        "role": role,
        "exp": expire,
    }
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role")
        
        if user_id is None:
            return None
            
        return {"user_id": user_id, "email": email, "role": role}
    except JWTError:
        return None


async def get_or_create_user(email: str, name: str, password: str) -> dict:
    """Get or create user"""
    user = await db.fetchrow(
        "SELECT id, email, name, role FROM users WHERE email = $1",
        email,
    )
    
    if user:
        return dict(user)
    
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(password)
    
    await db.execute(
        """
        INSERT INTO users (id, email, name, password_hash, role, created_at)
        VALUES ($1, $2, $3, $4, $5, $6)
        """,
        user_id,
        email,
        name,
        hashed_password,
        "user",
        datetime.utcnow(),
    )
    
    return {
        "id": user_id,
        "email": email,
        "name": name,
        "role": "user",
    }


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticate user with email and password"""
    user = await db.fetchrow(
        "SELECT id, email, name, password_hash, role FROM users WHERE email = $1",
        email,
    )
    
    if not user:
        return None
    
    if not verify_password(password, user["password_hash"]):
        return None
    
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
    }
