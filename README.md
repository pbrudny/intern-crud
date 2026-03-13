# Intern CRUD - Student Intern Profile Management System

A web-based CRUD application for managing student intern profiles, built with Python 3.14 and Flask.

## Overview

The intern-crud application allows students to create and manage their intern profiles, which can be viewed by authenticated users (companies, administrators, other students). The system includes user authentication, role-based access control, profile management with file uploads, and administrative functions.

## Features

- ✅ **User Authentication**: Secure login/registration with session management
- ✅ **Student Profiles**: Create, read, update, delete intern profiles
- ✅ **File Uploads**: PDF resume uploads (max 2MB)
- ✅ **Role-Based Access**: Regular users and administrators
- ✅ **Admin Management**: First user auto-promoted to admin, can promote others
- ✅ **Form Validation**: Comprehensive validation with CSRF protection
- ✅ **Responsive UI**: Bootstrap 5 for mobile-friendly interface

## Tech Stack

- **Language**: Python 3.14
- **Framework**: Flask
- **Database**: SQLite (development), PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Forms**: WTForms + Flask-WTF
- **Templates**: Jinja2
- **CSS**: Bootstrap 5
- **Testing**: pytest
- **Package Manager**: UV (modern, fast Python package manager)

## Quick Start

### Prerequisites

- Python 3.14
- UV package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Setup (2 minutes)

```bash
# Clone the repository
git clone git@github.com:pbrudny/intern-crud.git
cd intern-crud

# Install dependencies (UV automatically creates venv)
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
uv run flask db init
uv run flask db migrate -m "Initial migration"
uv run flask db upgrade

# Run the application
uv run flask run
```

Visit `http://localhost:5000`

## Development

### Run Tests

```bash
uv run pytest
uv run pytest --cov=app tests/
```

### Database Migrations

```bash
uv run flask db migrate -m "Description"
uv run flask db upgrade
```

### Add Dependencies

```bash
uv add package-name
uv add --dev package-name  # Dev dependencies
```

## Project Structure

```
intern-crud/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── auth/            # Authentication blueprint
│   │   ├── profiles/        # Profile management blueprint
│   │   ├── admin/           # Admin blueprint
│   │   ├── static/          # CSS, JS, images
│   │   └── templates/       # Jinja2 templates
│   ├── migrations/          # Database migrations
│   ├── tests/               # Test suite
│   ├── config.py
│   └── run.py
├── specs/                   # Feature specifications
│   └── 001-intern-crud-app/
│       ├── spec.md          # Feature specification
│       ├── plan.md          # Implementation plan
│       ├── research.md      # Technical decisions
│       ├── data-model.md    # Database schema
│       ├── quickstart.md    # Developer guide
│       └── contracts/       # API contracts
├── pyproject.toml           # Dependencies
├── uv.lock                  # Lockfile
└── .env                     # Environment variables
```

## Documentation

- **[Feature Specification](specs/001-intern-crud-app/spec.md)** - Complete feature requirements
- **[Implementation Plan](specs/001-intern-crud-app/plan.md)** - Technical architecture and decisions
- **[Quickstart Guide](specs/001-intern-crud-app/quickstart.md)** - Detailed setup instructions
- **[Data Model](specs/001-intern-crud-app/data-model.md)** - Database schema and entities
- **[Routes Contract](specs/001-intern-crud-app/contracts/routes.md)** - HTTP endpoints

## User Roles

- **Regular User**: Can create/edit/delete their own profile, view all profiles
- **Administrator**: Can edit/delete any profile, promote/revoke admin roles
- **First User**: Automatically becomes administrator

## Profile Fields

**Required**:
- Name
- Email
- Student Index Number (alphanumeric, min 4 chars)
- Institution
- Field of Study
- Graduation Date

**Optional**:
- Work Experience
- Projects
- LinkedIn URL
- Availability
- Preferred Locations
- Resume (PDF, max 2MB)

## Security

- Password hashing (PBKDF2)
- CSRF protection
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (Jinja2 auto-escaping)
- File upload validation
- Secure session cookies
- Role-based authorization

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Contact

[Add contact information here]

