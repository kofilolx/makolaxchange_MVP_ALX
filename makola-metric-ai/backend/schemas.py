from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# Auth Schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# Conversion Schemas
class ConversionRequest(BaseModel):
    amount: float
    fromCurrency: str
    toCurrency: str


class ConversionResponse(BaseModel):
    id: str
    user_id: str
    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float
    rate: float
    confidence: float
    timestamp: datetime


class ConversionHistory(BaseModel):
    conversions: list[ConversionResponse]
    total_count: int


# Regional Analysis Schemas
class RegionalAnalysis(BaseModel):
    region: str
    avg_rate: float
    total_volume: float
    conversion_count: int
    top_currency_pairs: list[dict]
    confidence_trend: list[float]


# Admin Schemas
class AdminStats(BaseModel):
    total_users: int
    total_conversions: int
    total_volume: float
    avg_confidence: float
    conversions_today: int
    active_users_today: int


class AdminUser(BaseModel):
    id: str
    email: str
    name: str
    conversions_count: int
    created_at: datetime


class AdminUsersResponse(BaseModel):
    users: list[AdminUser]
    total_count: int
