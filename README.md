# CampusConnect

A modern, full-stack college event management system with authentication, role-based access control, QR code tickets, and certificate generation.

## Features

- **User Authentication**: Secure JWT-based authentication with password hashing
- **Role-Based Access Control**: Student, Organizer, and Admin roles with appropriate permissions
- **Event Management**: Create, edit, delete, and browse campus events
- **Event Registration**: Users can register for events with capacity checks
- **QR Code Tickets**: Automatic QR code generation for event registrations
- **Certificate Generation**: PDF certificates for event participants
- **Admin Panel**: Comprehensive dashboard for managing users, events, and registrations
- **Dark Mode**: Full dark mode support
- **Responsive Design**: Mobile-friendly UI with modern design

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Database (can be swapped for PostgreSQL/MySQL)
- **python-jose**: JWT token handling
- **passlib**: Password hashing with bcrypt
- **qrcode**: QR code generation
- **reportlab**: PDF certificate generation

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality UI components

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create environment file:
```bash
cp .env.example .env
```

6. Edit `.env` and set your configuration:
```env
DATABASE_URL=sqlite:///./campus_connect.db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env.local
```

4. Edit `.env.local` and set your configuration:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

## Running the Application

### Start the Backend

1. With the virtual environment activated:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Start the Frontend

1. In a new terminal:
```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## User Roles

- **Student**: Can browse events, register for events, view their registrations, download QR codes and certificates
- **Organizer**: Can create, edit, and delete their own events
- **Admin**: Full access to all features including admin panel for managing users, events, and registrations

## Default Admin Account

To create an admin account, register a new user and manually set the role to "admin" in the database, or use the API to create one.

## Project Structure

```
CampusConnect/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── admin.py       # Admin endpoints
│   │   │       ├── dashboard.py   # Dashboard stats
│   │   │       ├── events.py      # Event CRUD
│   │   │       ├── registrations.py # Event registration, QR, certificates
│   │   │       └── users.py       # Auth & user management
│   │   ├── core/
│   │   │   ├── config.py         # Configuration
│   │   │   ├── dependencies.py   # RBAC dependencies
│   │   │   └── security.py       # JWT & password hashing
│   │   ├── db/
│   │   │   ├── database.py       # Database connection
│   │   │   └── models.py         # SQLAlchemy models
│   │   └── schemas.py            # Pydantic schemas
│   ├── main.py                   # FastAPI app
│   ├── requirements.txt          # Python dependencies
│   └── .env.example              # Environment template
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── admin/           # Admin panel
│   │   │   ├── create-event/    # Event creation
│   │   │   ├── dashboard/       # User dashboard
│   │   │   ├── events/          # Event listing & details
│   │   │   ├── login/           # Login page
│   │   │   └── my-events/       # User registrations
│   │   ├── components/
│   │   │   ├── Navbar.tsx       # Navigation bar
│   │   │   ├── Skeleton.tsx     # Loading states
│   │   │   └── Toast.tsx        # Notifications
│   │   ├── lib/
│   │   │   ├── api.ts           # API utilities
│   │   │   └── auth.ts          # Auth utilities
│   │   ├── services/
│   │   │   └── eventService.ts  # Event API service
│   │   └── types/
│   │       └── index.ts         # TypeScript types
│   ├── middleware.ts            # Route protection
│   ├── package.json
│   └── .env.example              # Environment template
└── README.md
```

## Security Notes

- Change the `SECRET_KEY` in the backend `.env` file before production deployment
- Use environment variables for all sensitive configuration
- Enable HTTPS in production
- Implement rate limiting for API endpoints
- Add input validation and sanitization
- Use a production-grade database (PostgreSQL/MySQL) instead of SQLite

## License

This project is licensed under the MIT License.
