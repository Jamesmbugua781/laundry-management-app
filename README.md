# laundry-management-app

# Campus Laundry Management System (O2O Platform)

A production-grade Laundry Management Backend System designed to digitize campus laundry operations using modern backend engineering practices.

This platform transforms traditional offline laundry workflows into a seamless online experience for students and laundry vendors.

---

# Problem Statement

Most campus laundry businesses still operate manually:

- Students physically walk to laundry shops to check availability.
- Pricing is inconsistent or unclear.
- Laundry tracking is unreliable.
- Payment and debt records are poorly managed.
- Communication between vendors and students is inefficient.

This project solves these operational challenges through a scalable backend system built with modern software engineering standards.

---

# Project Goals

Build a reliable, scalable, secure, and production-ready backend platform that supports:

- Digital laundry service catalogs
- Real-time order tracking
- Payment and debt management
- SMS & email notifications
- M-Pesa integration
- Vendor operational analytics
- Production deployment workflows

---

# Tech Stack

## Backend
- FastAPI
- Python 3.12+

## Database
- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations

## Caching & Rate Limiting
- Redis
- SlowAPI

## Authentication & Security
- JWT Authentication
- Argon2 Password Hashing
- RBAC (Role-Based Access Control)

## Async & Background Tasks
- FastAPI Background Tasks

## Logging & Monitoring
- Loguru

## External APIs
- Africa's Talking (SMS)
- Resend (Emails)
- Safaricom Daraja API (M-Pesa Sandbox)

## DevOps
- Docker
- GitHub Actions
- Render / Railway Deployment

---

# Core Features

## 1. Digital Laundry Catalog

Students can:

- View laundry services
- Check pricing
- Browse item categories

### Engineering Standards
- Redis caching
- Optimized PostgreSQL queries
- Reduced API latency

---

## 2. Real-Time Laundry Tracking

Students can track orders using:

- Student ID
- Unique Order Code

### Status Flow
```text
QUEUED → WASHING → READY
```


 ###External APIs
- Africa's Talking (SMS)
- Resend (Emails)
- Safaricom Daraja API (M-Pesa Sandbox)

---

# Project Structure

The project follows a clean architecture pattern with a modular design:

- **`app/main.py`**: FastAPI application entry point and configuration.
- **`app/core/`**: Application-wide settings, Redis client, and SlowAPI rate limiter.
- **`app/apps/`**: Modular feature components (e.g., `auth`, `users`, `catalog`, `orders`, `finance`, `notifications`, `payments`).
- **`app/shared/`**: Shared utilities, custom exceptions, and base repository implementations.
- **`tests/`**: Pytest test suite for unit and integration testing.
- **`alembic/`**: Database migration scripts.

---

# Authentication

The application implements robust security:

- **JWT (JSON Web Tokens)**: Secure token-based authentication for all protected endpoints.
- **Argon2 Hashing**: State-of-the-art password hashing.
- **RBAC**: Role-Based Access Control to distinguish between student users and administrative/vendor users.

---

# Getting Started

## Prerequisites

- **Python 3.12+**
- **PostgreSQL**: Running instance of PostgreSQL database.
- **Redis**: Running instance for caching and rate-limiting.

## Installation & Virtual Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/laundry-management-app.git
   cd laundry-management-app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the root directory and configure the required variables. Do NOT commit real secrets to version control.

```env
APP_NAME="Laundry Management System"
DEBUG=True
DATABASE_URL="postgresql://user:password@localhost/dbname"
SECRET_KEY="your-secure-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# M-Pesa APIs
CONSUMER_KEY="your_consumer_key"
CONSUMER_SECRET="your_consumer_secret"
BUSINESS_SHORTCODE="your_shortcode"
PASSKEY="your_passkey"
ENVIRONMENT="sandbox"

# Notifications
RESEND_API_KEY="your_resend_api_key"
AFRICA'S_TALKING_API_KEY="your_at_api_key"
```

## Database Migrations

Apply the Alembic migrations to set up your PostgreSQL schema:

```bash
alembic upgrade head
```

To create a new migration after updating SQLAlchemy models:
```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Running the Server

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

---

# API Documentation

Once the server is running, FastAPI automatically generates interactive documentation:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

# Example API Usage

Test the health check endpoint using `curl`:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json'
```

**Expected Response:**
```json
{
  "message": "Laundry Management API is running",
  "status": "ok"
}
```

---

# Testing

Run the automated test suite using `pytest`:

```bash
pytest tests/
```

---

# Docker Usage

*Docker support is planned as part of the DevOps roadmap.*
Once available, you will be able to run the full stack via:

```bash
docker-compose up -d --build
```

---

# Deployment

The platform is designed to be deployed to **Render** or **Railway** using continuous deployment pipelines (GitHub Actions). Ensure all environment variables are securely configured in your hosting provider's dashboard.

---

# Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

# License

This project is proprietary or pending licensing. Please consult the maintainers before redistribution or commercial use.
