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
