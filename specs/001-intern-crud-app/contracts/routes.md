# Web Application Routes Contract

**Date**: 2026-03-13  
**Feature**: 001-intern-crud-app  
**Type**: Web Service Routes

## Overview

This document defines the HTTP routes (endpoints) exposed by the intern-crud web application. These routes represent the public interface that users interact with through their browsers.

## Authentication Routes

### Register

**Route**: `GET /auth/register`  
**Purpose**: Display registration form  
**Authentication**: Not required  
**Response**: HTML registration form

---

**Route**: `POST /auth/register`  
**Purpose**: Create new user account  
**Authentication**: Not required  
**Form Data**:
```
email: string (required, valid email)
password: string (required, min 8 chars)
confirm_password: string (required, must match password)
```
**Success Response**: Redirect to `/auth/login` with success message  
**Error Response**: Re-render form with validation errors  
**Side Effects**: 
- Creates User record
- First user gets `is_admin = True`
- Session created and user logged in

---

### Login

**Route**: `GET /auth/login`  
**Purpose**: Display login form  
**Authentication**: Not required  
**Response**: HTML login form

---

**Route**: `POST /auth/login`  
**Purpose**: Authenticate user  
**Authentication**: Not required  
**Form Data**:
```
email: string (required)
password: string (required)
remember_me: boolean (optional)
```
**Success Response**: Redirect to `/profiles/` (profile list)  
**Error Response**: Re-render form with error message  
**Side Effects**: Creates user session

---

### Logout

**Route**: `GET /auth/logout`  
**Purpose**: End user session  
**Authentication**: Required  
**Response**: Redirect to `/auth/login` with success message  
**Side Effects**: Destroys user session

---

## Profile Routes

### List Profiles

**Route**: `GET /profiles/`  
**Purpose**: Display list of all student profiles  
**Authentication**: Required  
**Query Parameters**: None (future: filtering, pagination)  
**Response**: HTML page with profile list  
**Permissions**: Any authenticated user

---

### View Profile

**Route**: `GET /profiles/<int:profile_id>`  
**Purpose**: Display detailed view of a single profile  
**Authentication**: Required  
**URL Parameters**:
```
profile_id: integer (required, must exist)
```
**Response**: HTML page with profile details  
**Error Response**: 404 if profile not found  
**Permissions**: Any authenticated user

---

### Create Profile (Form)

**Route**: `GET /profiles/create`  
**Purpose**: Display profile creation form  
**Authentication**: Required  
**Response**: HTML profile creation form  
**Permissions**: Any authenticated user without existing profile  
**Error Response**: Redirect to edit if user already has profile

---

**Route**: `POST /profiles/create`  
**Purpose**: Create new student profile  
**Authentication**: Required  
**Form Data**:
```
name: string (required, max 100)
email: string (required, valid email)
index_number: string (required, alphanumeric, min 4)
institution: string (required, max 200)
field_of_study: string (required, max 200)
graduation_date: date (required)
work_experience: text (optional, max 5000)
projects: text (optional, max 5000)
linkedin_url: string (optional, valid URL)
availability: string (optional, max 100)
locations: string (optional, max 255)
resume: file (optional, PDF, max 2MB)
```
**Success Response**: Redirect to `/profiles/<profile_id>` with success message  
**Error Response**: Re-render form with validation errors  
**Permissions**: User must not already have a profile  
**Side Effects**: 
- Creates StudentProfile record
- Uploads resume file if provided

---

### Edit Profile (Form)

**Route**: `GET /profiles/<int:profile_id>/edit`  
**Purpose**: Display profile edit form  
**Authentication**: Required  
**URL Parameters**:
```
profile_id: integer (required, must exist)
```
**Response**: HTML profile edit form pre-filled with current data  
**Permissions**: Profile owner OR administrator  
**Error Response**: 403 if not authorized, 404 if not found

---

**Route**: `POST /profiles/<int:profile_id>/edit`  
**Purpose**: Update existing student profile  
**Authentication**: Required  
**URL Parameters**:
```
profile_id: integer (required, must exist)
```
**Form Data**: Same as create profile  
**Success Response**: Redirect to `/profiles/<profile_id>` with success message  
**Error Response**: Re-render form with validation errors  
**Permissions**: Profile owner OR administrator  
**Side Effects**: 
- Updates StudentProfile record
- Updates `updated_at` timestamp
- Replaces resume file if new one uploaded

---

### Delete Profile

**Route**: `POST /profiles/<int:profile_id>/delete`  
**Purpose**: Delete student profile  
**Authentication**: Required  
**URL Parameters**:
```
profile_id: integer (required, must exist)
```
**Form Data**:
```
confirm: string (required, must be "yes")
```
**Success Response**: Redirect to `/profiles/` with success message  
**Error Response**: 403 if not authorized, 404 if not found  
**Permissions**: Profile owner OR administrator  
**Side Effects**: 
- Deletes StudentProfile record
- Deletes associated resume file

---

## Admin Routes

### User Management

**Route**: `GET /admin/users`  
**Purpose**: Display list of all users  
**Authentication**: Required  
**Response**: HTML page with user list  
**Permissions**: Administrator only  
**Error Response**: 403 if not admin

---

### Promote User to Admin

**Route**: `POST /admin/users/<int:user_id>/promote`  
**Purpose**: Grant administrator role to user  
**Authentication**: Required  
**URL Parameters**:
```
user_id: integer (required, must exist)
```
**Success Response**: Redirect to `/admin/users` with success message  
**Error Response**: 403 if not admin, 404 if user not found  
**Permissions**: Administrator only  
**Side Effects**: Sets `is_admin = True` for target user

---

### Revoke Admin Role

**Route**: `POST /admin/users/<int:user_id>/revoke`  
**Purpose**: Remove administrator role from user  
**Authentication**: Required  
**URL Parameters**:
```
user_id: integer (required, must exist)
```
**Success Response**: Redirect to `/admin/users` with success message  
**Error Response**: 
- 403 if not admin
- 400 if trying to revoke own admin role
- 404 if user not found  
**Permissions**: Administrator only  
**Validation**: Cannot revoke own admin role  
**Side Effects**: Sets `is_admin = False` for target user

---

## Static Routes

### Home Page

**Route**: `GET /`  
**Purpose**: Application home page  
**Authentication**: Not required  
**Response**: HTML landing page with links to login/register  
**Behavior**: If authenticated, redirect to `/profiles/`

---

### Resume Download

**Route**: `GET /uploads/resumes/<int:user_id>/<filename>`  
**Purpose**: Download resume file  
**Authentication**: Required  
**URL Parameters**:
```
user_id: integer (required)
filename: string (required, must be PDF)
```
**Response**: PDF file download  
**Error Response**: 404 if file not found, 403 if not authorized  
**Permissions**: Any authenticated user  
**Security**: Validate file path to prevent directory traversal

---

## Error Routes

### 404 Not Found

**Route**: Any undefined route  
**Response**: HTML 404 error page

---

### 403 Forbidden

**Route**: Triggered by permission checks  
**Response**: HTML 403 error page

---

### 500 Internal Server Error

**Route**: Triggered by unhandled exceptions  
**Response**: HTML 500 error page  
**Behavior**: Log error details, show generic message to user

---

## Route Summary

| Route | Method | Auth Required | Admin Only | Purpose |
|-------|--------|---------------|------------|---------|
| `/` | GET | No | No | Home page |
| `/auth/register` | GET, POST | No | No | User registration |
| `/auth/login` | GET, POST | No | No | User login |
| `/auth/logout` | GET | Yes | No | User logout |
| `/profiles/` | GET | Yes | No | List all profiles |
| `/profiles/<id>` | GET | Yes | No | View profile |
| `/profiles/create` | GET, POST | Yes | No | Create profile |
| `/profiles/<id>/edit` | GET, POST | Yes | Owner/Admin | Edit profile |
| `/profiles/<id>/delete` | POST | Yes | Owner/Admin | Delete profile |
| `/admin/users` | GET | Yes | Yes | User management |
| `/admin/users/<id>/promote` | POST | Yes | Yes | Promote to admin |
| `/admin/users/<id>/revoke` | POST | Yes | Yes | Revoke admin |
| `/uploads/resumes/<user_id>/<file>` | GET | Yes | No | Download resume |

---

## Security Considerations

1. **CSRF Protection**: All POST routes require CSRF token (Flask-WTF)
2. **Authentication**: Flask-Login session management
3. **Authorization**: Permission checks before sensitive operations
4. **File Upload**: Validate file type, size, and sanitize filenames
5. **SQL Injection**: SQLAlchemy ORM prevents injection
6. **XSS Prevention**: Jinja2 auto-escapes template variables
7. **Session Security**: Secure cookies, HTTPOnly flag

---

## Future Enhancements

- Pagination for profile list
- Search and filtering
- Profile export (PDF/CSV)
- Email verification
- Password reset
- API endpoints (JSON responses)

