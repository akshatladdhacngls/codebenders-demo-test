# Flight Booking Backend API

## Project Overview
A FastAPI-based backend for a flight booking system with comprehensive API endpoints for users, flights, bookings, and fares.

## Tech Stack
- Framework: FastAPI (0.104.1)
- Database: SQLite with SQLAlchemy ORM
- Python Version: 3.11+

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run Database Migrations
```bash
# Automatically handled by SQLAlchemy on first run
```

### 4. Start Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Users
- POST /users: Create a new user
- GET /users/{user_id}: Retrieve user details

### Flights
- GET /flights: Search available flights
- GET /flights/{flight_id}: Retrieve flight details

### Bookings
- POST /bookings: Create a new booking
- GET /bookings/{booking_id}: Retrieve booking details

### Fares
- GET /fares: List all fare types
- GET /fares/{fare_id}: Retrieve specific fare details

## Environment Variables
- DATABASE_URL: Database connection string
- SERVER_HOST: Server host (default: 0.0.0.0)
- SERVER_PORT: Server port (default: 8000)
- DEBUG: Enable/disable debug mode

## Error Handling
Standard HTTP status codes with descriptive error messages.