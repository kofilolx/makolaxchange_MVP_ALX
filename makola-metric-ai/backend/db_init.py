"""Database initialization script"""
import asyncio
import os
from database import db


async def init_db():
    """Initialize database with required tables"""
    await db.connect()
    
    try:
        # Create users table (if not exists)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(36) PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'user',
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create conversions table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS conversions (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL REFERENCES users(id),
                amount DECIMAL(20, 2) NOT NULL,
                from_currency VARCHAR(3) NOT NULL,
                to_currency VARCHAR(3) NOT NULL,
                converted_amount DECIMAL(20, 2) NOT NULL,
                rate DECIMAL(20, 8) NOT NULL,
                confidence DECIMAL(3, 2) NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes for better query performance
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_conversions_user_id 
            ON conversions(user_id)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_conversions_timestamp 
            ON conversions(timestamp)
        """)
        
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_conversions_currency_pair 
            ON conversions(from_currency, to_currency)
        """)
        
        print("✓ Database initialized successfully")
        
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        raise
    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(init_db())
