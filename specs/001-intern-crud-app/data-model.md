# Data Model: Intern Profile Management System

**Date**: 2026-03-13  
**Feature**: 001-intern-crud-app

## Overview

This document defines the data entities, relationships, validation rules, and state transitions for the intern profile management system.

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ email (unique)  │
│ password_hash   │
│ is_admin        │
│ created_at      │
└────────┬────────┘
         │
         │ 1:1
         │
         ▼
┌─────────────────┐
│  StudentProfile │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ name            │
│ email           │
│ index_number    │
│ institution     │
│ field_of_study  │
│ graduation_date │
│ work_experience │
│ projects        │
│ linkedin_url    │
│ availability    │
│ locations       │
│ resume_filename │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

## Entities

### User

Represents an authenticated user account in the system.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique user identifier |
| email | String(120) | Unique, Not Null, Indexed | User's email address (used for login) |
| password_hash | String(255) | Not Null | Hashed password (PBKDF2) |
| is_admin | Boolean | Not Null, Default: False | Administrator flag |
| created_at | DateTime | Not Null, Default: now() | Account creation timestamp |

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Email must be unique across all users
- Password must be at least 8 characters before hashing
- First registered user automatically gets `is_admin = True`

**Relationships**:
- One-to-One with StudentProfile (optional - users can exist without profiles)

**Indexes**:
- Unique index on `email`
- Index on `is_admin` for permission checks

**State Transitions**:
```
[New User] → [Regular User] → [Administrator] (via promotion)
                    ↓
              [Deleted User] (cascade deletes profile)
```

---

### StudentProfile

Represents an intern candidate profile with personal, educational, and professional information.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | Primary Key, Auto-increment | Unique profile identifier |
| user_id | Integer | Foreign Key (User.id), Unique, Not Null | Owner of this profile |
| name | String(100) | Not Null | Student's full name |
| email | String(120) | Not Null | Student's contact email |
| index_number | String(50) | Not Null | Student index/ID number |
| institution | String(200) | Not Null | Educational institution name |
| field_of_study | String(200) | Not Null | Major/field of study |
| graduation_date | Date | Not Null | Expected or actual graduation date |
| work_experience | Text | Nullable | Work experience description |
| projects | Text | Nullable | Projects description |
| linkedin_url | String(255) | Nullable | LinkedIn profile URL |
| availability | String(100) | Nullable | Availability dates/period |
| locations | String(255) | Nullable | Preferred work locations |
| resume_filename | String(255) | Nullable | Stored resume file name |
| created_at | DateTime | Not Null, Default: now() | Profile creation timestamp |
| updated_at | DateTime | Not Null, Default: now() | Last update timestamp |

**Validation Rules**:

*Required Fields*:
- name: 1-100 characters, non-empty
- email: Valid email format
- index_number: Alphanumeric, minimum 4 characters
- institution: 1-200 characters, non-empty
- field_of_study: 1-200 characters, non-empty
- graduation_date: Valid date, not more than 10 years in the past or future

*Optional Fields*:
- work_experience: Max 5000 characters
- projects: Max 5000 characters
- linkedin_url: Valid URL format if provided
- availability: Max 100 characters
- locations: Max 255 characters
- resume_filename: PDF only, max 2MB file size

*Business Rules*:
- One profile per user (enforced by unique user_id foreign key)
- Profile email should match user email (recommended but not enforced)
- Resume file must be PDF format
- Resume file size must not exceed 2MB

**Relationships**:
- Many-to-One with User (each profile belongs to exactly one user)

**Indexes**:
- Unique index on `user_id`
- Index on `email` for search functionality
- Index on `institution` for filtering
- Index on `field_of_study` for filtering

**State Transitions**:
```
[Draft] → [Created] → [Updated]* → [Deleted]
              ↓
         [Published] (visible to authenticated users)
```

---

## File Storage Model

### Resume Files

**Storage Location**: `/uploads/resumes/{user_id}/`

**Naming Convention**: `{user_id}_{timestamp}_{original_name}.pdf`

**Metadata**:
- Stored in `StudentProfile.resume_filename`
- Original filename sanitized to prevent path traversal
- File extension validated (.pdf only)
- MIME type validated (application/pdf)

**Lifecycle**:
- Created: When profile is created or updated with resume
- Updated: Old file deleted, new file stored
- Deleted: When profile is deleted (cascade)

---

## Validation Summary

### User Entity Validation

```python
# Email validation
- Format: RFC 5322 compliant
- Uniqueness: Database constraint
- Example: student@university.edu

# Password validation
- Minimum length: 8 characters
- Hashed using: Werkzeug PBKDF2
- Never stored in plain text

# Admin flag
- Boolean: True/False
- First user: Automatically True
- Others: False by default
```

### StudentProfile Entity Validation

```python
# Required field validation
name: 1 <= len(name) <= 100
email: valid_email_format(email)
index_number: len(index_number) >= 4 and alphanumeric(index_number)
institution: 1 <= len(institution) <= 200
field_of_study: 1 <= len(field_of_study) <= 200
graduation_date: is_valid_date(graduation_date)

# Optional field validation
work_experience: len(work_experience) <= 5000 if provided
projects: len(projects) <= 5000 if provided
linkedin_url: is_valid_url(linkedin_url) if provided
availability: len(availability) <= 100 if provided
locations: len(locations) <= 255 if provided

# File validation
resume: 
  - extension == '.pdf'
  - size <= 2MB (2097152 bytes)
  - mime_type == 'application/pdf'
```

---

## Database Constraints

### Foreign Key Constraints

```sql
ALTER TABLE student_profile
ADD CONSTRAINT fk_student_profile_user
FOREIGN KEY (user_id) REFERENCES user(id)
ON DELETE CASCADE;
```

### Unique Constraints

```sql
-- User table
ALTER TABLE user ADD CONSTRAINT uq_user_email UNIQUE (email);

-- StudentProfile table
ALTER TABLE student_profile ADD CONSTRAINT uq_profile_user UNIQUE (user_id);
```

### Check Constraints

```sql
-- Ensure index_number has minimum length
ALTER TABLE student_profile
ADD CONSTRAINT chk_index_number_length
CHECK (LENGTH(index_number) >= 4);

-- Ensure graduation_date is reasonable
ALTER TABLE student_profile
ADD CONSTRAINT chk_graduation_date_range
CHECK (graduation_date BETWEEN DATE('now', '-10 years') AND DATE('now', '+10 years'));
```

---

## Migration Strategy

### Initial Schema (Migration 001)

1. Create `user` table
2. Create `student_profile` table
3. Add foreign key constraints
4. Add indexes
5. Add check constraints

### Future Migrations

- Add fields as needed
- Modify constraints
- Add new indexes for performance
- Data migrations for schema changes

---

## Summary

This data model supports:
- ✅ User authentication and authorization
- ✅ Role-based access control (admin vs regular users)
- ✅ One profile per user constraint
- ✅ Comprehensive validation rules
- ✅ File upload management
- ✅ Audit trail (created_at, updated_at)
- ✅ Data integrity through constraints
- ✅ Scalable indexing strategy

