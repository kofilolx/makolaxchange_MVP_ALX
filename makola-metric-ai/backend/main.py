from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uuid
from datetime import datetime

from database import db
from schemas import (
    UserLogin,
    UserRegister,
    UserResponse,
    TokenResponse,
    ConversionRequest,
    ConversionResponse,
    ConversionHistory,
    RegionalAnalysis,
    AdminStats,
    AdminUsersResponse,
    AdminUser,
)
from auth import (
    authenticate_user,
    get_or_create_user,
    create_access_token,
    verify_token,
)
from ai_utils import convert_currency, get_regional_data


# Dependency for getting current user from token
async def get_current_user(authorization: str = None):
    """Extract and verify JWT token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    user_data = await verify_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_data


async def get_admin_user(user_data: dict = Depends(get_current_user)):
    """Check if user is admin"""
    if user_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown"""
    # Startup
    await db.connect()
    print("✓ Database connected")
    
    yield
    
    # Shutdown
    await db.disconnect()
    print("✓ Database disconnected")


app = FastAPI(title="MakolaMetric AI API", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================== AUTH ENDPOINTS =====================

@app.post("/auth/register", response_model=TokenResponse)
async def register(data: UserRegister):
    """Register a new user"""
    existing_user = await db.fetchrow(
        "SELECT id FROM users WHERE email = $1",
        data.email,
    )
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
        )
    
    user = await get_or_create_user(data.email, data.name, data.password)
    
    token = create_access_token(user["id"], user["email"], user["role"])
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            role=user["role"],
            created_at=datetime.utcnow(),
        ),
    )


@app.post("/auth/login", response_model=TokenResponse)
async def login(data: UserLogin):
    """Login user"""
    user = await authenticate_user(data.email, data.password)
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )
    
    token = create_access_token(user["id"], user["email"], user["role"])
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            role=user["role"],
            created_at=datetime.utcnow(),
        ),
    )


@app.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(user_data: dict = Depends(get_current_user)):
    """Get current user information"""
    user = await db.fetchrow(
        "SELECT id, email, name, role, created_at FROM users WHERE id = $1",
        user_data["user_id"],
    )
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**dict(user))


@app.post("/auth/logout")
async def logout(user_data: dict = Depends(get_current_user)):
    """Logout user (token invalidation happens on client)"""
    return {"message": "Logged out successfully"}


# ===================== CONVERSION ENDPOINTS =====================

@app.post("/conversion/convert", response_model=ConversionResponse)
async def convert(
    data: ConversionRequest,
    user_data: dict = Depends(get_current_user),
):
    """Convert currency with AI confidence scoring"""
    conversion_id = str(uuid.uuid4())
    converted_amount, rate, confidence = convert_currency(
        data.amount,
        data.fromCurrency,
        data.toCurrency,
    )
    
    # Save conversion to database
    await db.execute(
        """
        INSERT INTO conversions 
        (id, user_id, amount, from_currency, to_currency, converted_amount, rate, confidence, timestamp)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """,
        conversion_id,
        user_data["user_id"],
        data.amount,
        data.fromCurrency.upper(),
        data.toCurrency.upper(),
        converted_amount,
        rate,
        confidence,
        datetime.utcnow(),
    )
    
    return ConversionResponse(
        id=conversion_id,
        user_id=user_data["user_id"],
        amount=data.amount,
        from_currency=data.fromCurrency.upper(),
        to_currency=data.toCurrency.upper(),
        converted_amount=converted_amount,
        rate=rate,
        confidence=confidence,
        timestamp=datetime.utcnow(),
    )


@app.get("/conversion/history", response_model=ConversionHistory)
async def get_history(
    user_data: dict = Depends(get_current_user),
    limit: int = 50,
):
    """Get user's conversion history"""
    conversions = await db.fetch(
        """
        SELECT id, user_id, amount, from_currency, to_currency, 
               converted_amount, rate, confidence, timestamp
        FROM conversions
        WHERE user_id = $1
        ORDER BY timestamp DESC
        LIMIT $2
        """,
        user_data["user_id"],
        limit,
    )
    
    total_count = await db.fetchval(
        "SELECT COUNT(*) FROM conversions WHERE user_id = $1",
        user_data["user_id"],
    )
    
    return ConversionHistory(
        conversions=[ConversionResponse(**dict(c)) for c in conversions],
        total_count=total_count,
    )


@app.get("/conversion/analysis/regional/{region}", response_model=RegionalAnalysis)
async def get_regional_analysis(
    region: str,
    user_data: dict = Depends(get_current_user),
):
    """Get regional analysis for currency conversions"""
    data = get_regional_data(region)
    
    return RegionalAnalysis(
        region=region,
        avg_rate=data["avg_rate"],
        total_volume=data["total_volume"],
        conversion_count=data["conversion_count"],
        top_currency_pairs=[
            {"from": pair[0], "to": pair[1]} for pair in data["top_pairs"]
        ],
        confidence_trend=data["confidence_trend"],
    )


# ===================== ADMIN ENDPOINTS =====================

@app.get("/admin/stats", response_model=AdminStats)
async def get_admin_stats(admin_user: dict = Depends(get_admin_user)):
    """Get system statistics (admin only)"""
    total_users = await db.fetchval("SELECT COUNT(*) FROM users")
    total_conversions = await db.fetchval("SELECT COUNT(*) FROM conversions")
    total_volume = await db.fetchval(
        "SELECT COALESCE(SUM(amount), 0) FROM conversions"
    )
    avg_confidence = await db.fetchval(
        "SELECT COALESCE(AVG(confidence), 0) FROM conversions"
    )
    
    # Conversions today
    conversions_today = await db.fetchval(
        """
        SELECT COUNT(*) FROM conversions 
        WHERE DATE(timestamp) = CURRENT_DATE
        """
    )
    
    # Active users today
    active_users_today = await db.fetchval(
        """
        SELECT COUNT(DISTINCT user_id) FROM conversions
        WHERE DATE(timestamp) = CURRENT_DATE
        """
    )
    
    return AdminStats(
        total_users=total_users,
        total_conversions=total_conversions,
        total_volume=float(total_volume),
        avg_confidence=float(avg_confidence),
        conversions_today=conversions_today,
        active_users_today=active_users_today,
    )


@app.get("/admin/users", response_model=AdminUsersResponse)
async def get_admin_users(
    admin_user: dict = Depends(get_admin_user),
    limit: int = 100,
):
    """Get all users (admin only)"""
    users = await db.fetch(
        """
        SELECT u.id, u.email, u.name, u.created_at,
               COUNT(c.id) as conversions_count
        FROM users u
        LEFT JOIN conversions c ON u.id = c.user_id
        GROUP BY u.id
        ORDER BY u.created_at DESC
        LIMIT $1
        """,
        limit,
    )
    
    total_count = await db.fetchval("SELECT COUNT(*) FROM users")
    
    return AdminUsersResponse(
        users=[AdminUser(**dict(u)) for u in users],
        total_count=total_count,
    )


# ===================== HEALTH CHECK =====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "makola-metric-api"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
