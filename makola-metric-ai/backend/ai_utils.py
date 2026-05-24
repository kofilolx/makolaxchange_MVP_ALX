import random
from datetime import datetime, timedelta
from typing import Tuple


# Simulated exchange rates for demo purposes
EXCHANGE_RATES = {
    ("USD", "EUR"): 0.92,
    ("USD", "GBP"): 0.79,
    ("USD", "JPY"): 149.50,
    ("EUR", "USD"): 1.09,
    ("EUR", "GBP"): 0.86,
    ("EUR", "JPY"): 162.50,
    ("GBP", "USD"): 1.27,
    ("GBP", "EUR"): 1.16,
    ("GBP", "JPY"): 189.00,
    ("JPY", "USD"): 0.0067,
    ("JPY", "EUR"): 0.0062,
    ("JPY", "GBP"): 0.0053,
}


def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Get exchange rate between two currencies"""
    key = (from_currency.upper(), to_currency.upper())
    
    if key in EXCHANGE_RATES:
        # Add slight variation to simulate real market rates
        base_rate = EXCHANGE_RATES[key]
        variation = random.uniform(0.98, 1.02)
        return base_rate * variation
    
    # Fallback for other pairs
    return 1.0


def calculate_confidence(
    from_currency: str,
    to_currency: str,
    amount: float,
) -> float:
    """
    Calculate confidence score for conversion (0.0 to 1.0).
    Factors:
    - Rate freshness (assumed recent)
    - Currency pair liquidity
    - Amount size
    - Historical volatility
    """
    confidence = 0.85  # Base confidence
    
    # Major pairs get higher confidence
    major_pairs = {
        ("USD", "EUR"),
        ("USD", "GBP"),
        ("USD", "JPY"),
        ("EUR", "GBP"),
        ("EUR", "JPY"),
        ("GBP", "JPY"),
    }
    
    pair = (from_currency.upper(), to_currency.upper())
    if pair in major_pairs or (pair[1], pair[0]) in major_pairs:
        confidence += 0.10
    
    # Moderate amounts get higher confidence
    if 100 <= amount <= 1000000:
        confidence += 0.05
    
    # Cap at 1.0
    confidence = min(confidence, 1.0)
    
    # Simulate some variance
    variance = random.uniform(0.95, 1.0)
    return confidence * variance


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> Tuple[float, float, float]:
    """
    Convert currency and return (converted_amount, rate, confidence).
    """
    if from_currency.upper() == to_currency.upper():
        return amount, 1.0, 1.0
    
    rate = get_exchange_rate(from_currency, to_currency)
    converted_amount = amount * rate
    confidence = calculate_confidence(from_currency, to_currency, amount)
    
    return converted_amount, rate, confidence


def get_regional_data(region: str) -> dict:
    """Get simulated regional analysis data"""
    regions = {
        "north_america": {
            "avg_rate": 1.0,
            "total_volume": 5000000,
            "conversion_count": 15000,
            "top_pairs": [("USD", "CAD"), ("USD", "MXN")],
        },
        "europe": {
            "avg_rate": 0.92,
            "total_volume": 3000000,
            "conversion_count": 10000,
            "top_pairs": [("EUR", "GBP"), ("EUR", "CHF")],
        },
        "asia_pacific": {
            "avg_rate": 1.5,
            "total_volume": 4000000,
            "conversion_count": 12000,
            "top_pairs": [("USD", "JPY"), ("USD", "CNY")],
        },
    }
    
    data = regions.get(region.lower(), regions["north_america"])
    
    # Add some variance
    data["avg_rate"] *= random.uniform(0.99, 1.01)
    data["total_volume"] *= random.uniform(0.95, 1.05)
    data["confidence_trend"] = [
        random.uniform(0.80, 0.95) for _ in range(24)
    ]  # Hourly trend
    
    return data
