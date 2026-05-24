# MakolaMetric AI - Currency Conversion Platform

An AI-powered currency conversion platform built with FastAPI backend and Next.js frontend, featuring intelligent confidence scoring and conversion history tracking.

## Architecture

This project uses Vercel's `experimentalServices` API to run a multi-service application:

- **Backend**: FastAPI (Python) - Serverless functions for currency conversion and API
- **Frontend**: Next.js (React) - User interface for conversion and history
- **Database**: Neon PostgreSQL - Data persistence and user management
- **Deployment**: Vercel with automatic multi-service orchestration

## Project Structure

```
.
├── backend/                    # FastAPI backend
│   ├── main.py               # API routes
│   ├── database.py           # Database connection
│   ├── auth.py               # Authentication utilities
│   ├── schemas.py            # Pydantic validation schemas
│   ├── ai_utils.py           # AI confidence scoring
│   ├── db_init.py            # Database initialization script
│   └── pyproject.toml        # Python dependencies
├── frontend/                   # Next.js frontend
│   ├── app/                  # Page routes
│   ├── components/           # React components
│   ├── lib/                  # Utilities
│   ├── package.json          # NPM dependencies
│   └── next.config.ts        # Next.js configuration
├── vercel.json              # Services configuration
└── README.md                # This file
```

## Features

### Core Functionality
- **Currency Conversion**: Convert between 10+ currencies (USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, INR, MXN)
- **AI Confidence Scoring**: Rule-based confidence calculation (0-100%) based on:
  - Exchange rate source quality
  - Data recency
  - Market volatility
  - User conversion history
- **Conversion History**: Track and manage past conversions with pagination
- **User Authentication**: Secure login/registration with JWT tokens

### Admin Features
- User management dashboard
- System analytics and conversion statistics
- Admin action logging

## Getting Started

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Neon PostgreSQL database (configured via integration)

### Installation

1. **Install dependencies**:
   ```bash
   # Frontend
   cd frontend
   pnpm install
   cd ..
   
   # Backend (done automatically by Vercel)
   ```

2. **Set up environment variables**:
   Copy `.env.example` to `.env.local` and fill in:
   - `DATABASE_URL` (from Neon integration)
   - `JWT_SECRET` (generate a strong random key)
   - `NEON_AUTH_COOKIE_SECRET` (from integration setup)

3. **Initialize database**:
   ```bash
   # Run the database initialization script
   python backend/db_init.py
   ```

### Development

The project runs automatically on Vercel preview with multi-service support:

```bash
# Frontend runs on :3000
# Backend API runs on :3000/api (routed via Vercel)
```

No manual `vercel dev` is needed - Vercel handles service orchestration.

## API Routes

### Authentication
- `POST /api/auth/register` - Create new account
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Conversions
- `POST /api/conversions` - Create conversion
- `GET /api/conversions` - List user conversions (paginated)
- `GET /api/conversions/{id}` - Get conversion details
- `DELETE /api/conversions/{id}` - Delete conversion

### Admin (requires admin role)
- `GET /api/admin/users` - List all users
- `GET /api/admin/conversions` - List all conversions
- `GET /api/admin/analytics` - System analytics
- `DELETE /api/admin/users/{id}` - Delete user

## Database Schema

### Tables
- **neon_auth.user** - User accounts (from auth integration)
- **public.conversions** - Conversion records
- **public.conversion_metadata** - Regional market data
- **public.admin_logs** - Admin action tracking

See `backend/db_init.py` for full schema definition.

## AI Confidence Scoring

The confidence score (0-100%) is calculated using a rule-based approach:

```
Confidence = (quality + recency + volatility + consistency) / 100 * 100

Where:
- Quality (0-20): Exchange rate source quality (major pairs = 20, others = 15)
- Recency (0-20): Data age (current data = 20)
- Volatility (0-30): Market stability (major pairs = 28, others = 22)
- Consistency (0-30): User history (0 conversions = 20, 10+ = 30)
```

## Deployment

Deploy to Vercel with automatic multi-service setup:

1. Connect GitHub repository to Vercel
2. Set environment variables in Vercel project settings
3. Configure build settings:
   - Framework Preset: Services
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/.next`
4. Deploy on push

## Environment Variables

### Required
- `DATABASE_URL` - PostgreSQL connection string (from Neon)
- `JWT_SECRET` - Secret for JWT token signing
- `NEON_AUTH_COOKIE_SECRET` - Cookie encryption key (from integration)

### Optional
- `NEXT_PUBLIC_API_BASE_URL` - Frontend API base URL (defaults to relative paths)

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Check Neon dashboard for active connections
- Ensure IP allowlist includes Vercel deployment IPs

### Authentication Errors
- Clear browser localStorage and try again
- Verify JWT_SECRET is set in environment
- Check token expiration (24 hours by default)

### Conversion API Errors
- Ensure user is authenticated (token in localStorage)
- Verify currency codes are valid ISO 4217 codes
- Check server logs for detailed error messages

## Performance Notes

- Conversions complete in <500ms
- Database queries use indexes for fast lookups
- Connection pooling for efficient resource usage
- Pagination limits to prevent large responses

## Development Notes

- No ORM used (direct SQL for performance)
- AsyncPG for async database operations
- FastAPI auto-generates OpenAPI documentation at `/docs`
- Next.js static optimization for frontend performance

## Future Enhancements

- Real exchange rate API integration (instead of mock data)
- ML-based confidence scoring with historical accuracy
- Real-time market data with WebSocket updates
- Advanced analytics dashboard with charts
- Mobile app with React Native

## License

MIT
