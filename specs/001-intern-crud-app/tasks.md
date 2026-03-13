# Tasks: Intern Profile Management System

**Input**: Design documents from `/specs/001-intern-crud-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/routes.md

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are excluded. Focus on implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md, this project uses:
- Backend: `backend/app/` for application code
- Config: `backend/config.py`
- Entry point: `backend/run.py`
- Dependencies: `pyproject.toml` (UV package manager)

---

## Phase 1: Setup (Shared Infrastructure) ✅ COMPLETE

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure per plan.md (backend/app/, backend/migrations/, backend/tests/, backend/uploads/resumes/)
- [X] T002 Initialize pyproject.toml with Python 3.14 and Flask dependencies (Flask, SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate, WTForms, email-validator, python-dotenv, Werkzeug)
- [X] T003 [P] Create .env.example file with required environment variables (SECRET_KEY, DATABASE_URL, FLASK_APP, FLASK_ENV, UPLOAD_FOLDER, MAX_CONTENT_LENGTH)
- [X] T004 [P] Create backend/config.py with configuration classes (DevelopmentConfig, ProductionConfig)
- [X] T005 [P] Create backend/run.py as application entry point
- [X] T006 [P] Create backend/app/__init__.py with Flask app factory pattern
- [X] T007 [P] Create backend/app/static/css/style.css for custom styles
- [X] T008 [P] Create backend/app/static/js/main.js for custom JavaScript
- [X] T009 [P] Create backend/app/templates/base.html with Bootstrap 5 layout and navigation
- [X] T010 [P] Create backend/app/templates/index.html for home page
- [X] T011 [P] Create backend/app/templates/errors/403.html for forbidden errors
- [X] T012 [P] Create backend/app/templates/errors/404.html for not found errors
- [X] T013 [P] Create backend/app/templates/errors/500.html for server errors
- [X] T014 Run uv sync to install dependencies and create virtual environment

---

## Phase 2: Foundational (Blocking Prerequisites) ✅ COMPLETE

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T015 Create backend/app/models/__init__.py to initialize SQLAlchemy db instance
- [X] T016 [P] Create backend/app/models/user.py with User model (id, email, password_hash, is_admin, created_at)
- [X] T017 [P] Create backend/app/models/profile.py with StudentProfile model (all fields from data-model.md)
- [X] T018 Initialize Flask-Migrate in backend/app/__init__.py
- [X] T019 Run uv run flask db init to create migrations directory
- [X] T020 Run uv run flask db migrate -m "Initial migration with User and StudentProfile models"
- [X] T021 Run uv run flask db upgrade to apply initial migration
- [X] T022 Create backend/app/auth/__init__.py to register authentication blueprint
- [X] T023 Create backend/app/auth/forms.py with LoginForm and RegistrationForm (WTForms)
- [X] T024 Implement backend/app/auth/routes.py with register route (GET/POST) - includes first user auto-admin logic
- [X] T025 Implement login route in backend/app/auth/routes.py (GET/POST) with Flask-Login session management
- [X] T026 Implement logout route in backend/app/auth/routes.py (GET)
- [X] T027 [P] Create backend/app/auth/templates/login.html with Bootstrap 5 form
- [X] T028 [P] Create backend/app/auth/templates/register.html with Bootstrap 5 form
- [X] T029 Configure Flask-Login in backend/app/__init__.py with user_loader callback
- [X] T030 Create authentication decorator/middleware for @login_required functionality
- [X] T031 Create permission checking utilities (is_owner_or_admin) in backend/app/auth/utils.py

**Checkpoint**: ✅ Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Student Profile Creation (Priority: P1) 🎯 MVP ✅ COMPLETE

**Goal**: Students can create their intern profile by filling out a form with personal and academic details

**Independent Test**: Register as a student, fill out profile form with all required fields, submit, verify profile is saved and can be viewed

### Implementation for User Story 1

- [X] T032 Create backend/app/profiles/__init__.py to register profiles blueprint
- [X] T033 [US1] Create backend/app/profiles/forms.py with ProfileForm (all fields from data-model.md with validation)
- [X] T034 [US1] Implement GET /profiles/create route in backend/app/profiles/routes.py (display form, check user doesn't have profile)
- [X] T035 [US1] Implement POST /profiles/create route in backend/app/profiles/routes.py (validate, save profile, handle resume upload)
- [X] T036 [US1] Add file upload validation in backend/app/profiles/routes.py (PDF only, max 2MB, sanitize filename)
- [X] T037 [US1] Add form field validation in backend/app/profiles/forms.py (index_number alphanumeric min 4 chars, email format, required fields)
- [X] T038 [US1] Create backend/app/profiles/templates/create.html with Bootstrap 5 form including file upload
- [X] T039 [US1] Add success/error flash messages for profile creation
- [X] T040 [US1] Create uploads/resumes/ directory structure with .gitkeep file

**Checkpoint**: ✅ User Story 1 is fully functional - students can register and create profiles - MVP COMPLETE!

---

## Phase 4: User Story 2 - Profile Viewing and Browsing (Priority: P2)

**Goal**: Authenticated users can view a list of all student profiles and access individual profile details

**Independent Test**: Create multiple profiles, log in as any authenticated user, access profile list, click on individual profiles to view details

### Implementation for User Story 2

- [ ] T041 [US2] Implement GET /profiles/ route in backend/app/profiles/routes.py (list all profiles, require authentication)
- [ ] T042 [US2] Implement GET /profiles/<int:profile_id> route in backend/app/profiles/routes.py (show profile details, require authentication)
- [ ] T043 [US2] Create backend/app/profiles/templates/list.html with Bootstrap 5 card layout for profile listing
- [ ] T044 [US2] Create backend/app/profiles/templates/view.html with Bootstrap 5 layout for profile details
- [ ] T045 [US2] Add resume download link in view.html template (if resume exists)
- [ ] T046 [US2] Implement GET /uploads/resumes/<user_id>/<filename> route for resume downloads (authentication required, file validation)
- [ ] T047 [US2] Add "No profiles available" message in list.html when no profiles exist
- [ ] T048 [US2] Add authentication redirect to login page for unauthenticated users accessing profile routes

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - profiles can be created and viewed

---

## Phase 5: User Story 3 - Profile Updates (Priority: P3)

**Goal**: Students can update their existing profile information; administrators can edit any profile

**Independent Test**: Create a profile, log in as profile owner, edit profile, verify changes are saved; log in as admin, edit another user's profile, verify changes are saved

### Implementation for User Story 3

- [ ] T049 [US3] Implement GET /profiles/<int:profile_id>/edit route in backend/app/profiles/routes.py (display edit form, check permissions)
- [ ] T050 [US3] Implement POST /profiles/<int:profile_id>/edit route in backend/app/profiles/routes.py (validate, update profile, handle resume replacement)
- [ ] T051 [US3] Add permission check in edit routes (owner or admin only) using is_owner_or_admin utility
- [ ] T052 [US3] Create backend/app/profiles/templates/edit.html with pre-filled form (reuse ProfileForm from create)
- [ ] T053 [US3] Add resume replacement logic (delete old file if new one uploaded) in edit route
- [ ] T054 [US3] Update updated_at timestamp on profile save
- [ ] T055 [US3] Add 403 Forbidden error handling for unauthorized edit attempts
- [ ] T056 [US3] Add success/error flash messages for profile updates

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - profiles can be created, viewed, and updated

---

## Phase 6: User Story 4 - Profile Deletion (Priority: P4)

**Goal**: Students can delete their own profile; administrators can delete any profile

**Independent Test**: Create a profile, log in as profile owner, delete profile with confirmation, verify it's removed; log in as admin, delete another user's profile, verify it's removed

### Implementation for User Story 4

- [ ] T057 [US4] Implement POST /profiles/<int:profile_id>/delete route in backend/app/profiles/routes.py (delete profile, check permissions)
- [ ] T058 [US4] Add permission check in delete route (owner or admin only)
- [ ] T059 [US4] Add confirmation dialog in view.html and edit.html templates (JavaScript confirm or modal)
- [ ] T060 [US4] Add resume file deletion when profile is deleted (cascade delete)
- [ ] T061 [US4] Add 403 Forbidden error handling for unauthorized delete attempts
- [ ] T062 [US4] Add success flash message after deletion and redirect to profile list
- [ ] T063 [US4] Handle edge case: prevent deletion if profile doesn't exist (404 error)

**Checkpoint**: At this point, User Stories 1-4 should all work independently - full CRUD operations on profiles

---

## Phase 7: User Story 5 - Administrator Management (Priority: P5)

**Goal**: First registered user becomes admin automatically; admins can promote/revoke admin roles for other users

**Independent Test**: Register first user, verify they are admin; as admin, promote another user, verify they gain admin privileges; revoke admin from a user, verify they lose privileges

### Implementation for User Story 5

- [ ] T064 Create backend/app/admin/__init__.py to register admin blueprint
- [ ] T065 [US5] Implement GET /admin/users route in backend/app/admin/routes.py (list all users, admin only)
- [ ] T066 [US5] Implement POST /admin/users/<int:user_id>/promote route in backend/app/admin/routes.py (set is_admin=True, admin only)
- [ ] T067 [US5] Implement POST /admin/users/<int:user_id>/revoke route in backend/app/admin/routes.py (set is_admin=False, prevent self-revoke, admin only)
- [ ] T068 [US5] Create backend/app/admin/templates/users.html with user list and promote/revoke buttons
- [ ] T069 [US5] Add admin-only decorator/check for all admin routes
- [ ] T070 [US5] Add validation to prevent admin from revoking their own admin role
- [ ] T071 [US5] Add success/error flash messages for promote/revoke operations
- [ ] T072 [US5] Add admin menu item in base.html navigation (visible only to admins)

**Checkpoint**: All user stories should now be independently functional - complete application with admin management

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T073 [P] Add navigation links in base.html (Home, Profiles, Create Profile, Admin, Login/Logout)
- [ ] T074 [P] Add conditional navigation display (show/hide based on authentication and admin status)
- [ ] T075 [P] Improve error messages across all forms for better user experience
- [ ] T076 [P] Add loading states and form submission feedback
- [ ] T077 [P] Implement proper error handling for file upload failures
- [ ] T078 [P] Add input sanitization for text fields to prevent XSS
- [ ] T079 [P] Add CSRF token validation to all forms (Flask-WTF handles this)
- [ ] T080 [P] Add proper HTTP status codes for all error responses
- [ ] T081 [P] Improve Bootstrap 5 styling consistency across all templates
- [ ] T082 [P] Add responsive design improvements for mobile devices
- [ ] T083 [P] Add favicon and meta tags in base.html
- [ ] T084 [P] Create README.md usage section with screenshots (optional)
- [ ] T085 Validate quickstart.md instructions by following them end-to-end
- [ ] T086 Add database indexes per data-model.md (email, user_id, is_admin)
- [ ] T087 Add logging for critical operations (user registration, profile creation, admin actions)
- [ ] T088 Security review: verify password hashing, CSRF protection, file upload validation
- [ ] T089 Performance review: check query efficiency, add eager loading where needed
- [ ] T090 Final testing: verify all 5 user stories work independently and together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 but builds on profile viewing
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Requires profile editing permissions
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Requires profile deletion permissions
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Independent admin functionality

### Within Each User Story

- Routes before templates
- Forms before routes (for validation)
- Permission checks before sensitive operations
- Core implementation before edge case handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003-T013)
- Models in Foundational phase can run in parallel (T016, T017)
- Templates in Foundational phase can run in parallel (T027, T028)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Polish tasks marked [P] can run in parallel (T073-T084)

---

## Parallel Example: Foundational Phase

```bash
# Launch all model creation together:
Task T016: "Create backend/app/models/user.py with User model"
Task T017: "Create backend/app/models/profile.py with StudentProfile model"

# Launch all template creation together:
Task T027: "Create backend/app/auth/templates/login.html"
Task T028: "Create backend/app/auth/templates/register.html"
```

---

## Parallel Example: User Story 1

```bash
# After form is created (T033), these can run in parallel:
Task T034: "Implement GET /profiles/create route"
Task T038: "Create backend/app/profiles/templates/create.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T014)
2. Complete Phase 2: Foundational (T015-T031) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T032-T040)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Register a user
   - Create a profile with all fields
   - Verify profile is saved
   - View the created profile
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T031)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!) (T032-T040)
3. Add User Story 2 → Test independently → Deploy/Demo (T041-T048)
4. Add User Story 3 → Test independently → Deploy/Demo (T049-T056)
5. Add User Story 4 → Test independently → Deploy/Demo (T057-T063)
6. Add User Story 5 → Test independently → Deploy/Demo (T064-T072)
7. Polish → Final release (T073-T090)

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T031)
2. Once Foundational is done:
   - Developer A: User Story 1 (T032-T040)
   - Developer B: User Story 2 (T041-T048)
   - Developer C: User Story 3 (T049-T056)
3. Stories complete and integrate independently
4. Continue with remaining stories (US4, US5) and polish

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Use `uv run` for all Flask commands (no manual venv activation needed)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- File paths are exact - follow plan.md structure
- Tests are not included as they were not explicitly requested in the specification
- Focus on implementation quality and user experience

---

## Task Count Summary

- **Total Tasks**: 90
- **Setup (Phase 1)**: 14 tasks
- **Foundational (Phase 2)**: 17 tasks (BLOCKING)
- **User Story 1 (Phase 3)**: 9 tasks
- **User Story 2 (Phase 4)**: 8 tasks
- **User Story 3 (Phase 5)**: 8 tasks
- **User Story 4 (Phase 6)**: 7 tasks
- **User Story 5 (Phase 7)**: 9 tasks
- **Polish (Phase 8)**: 18 tasks
- **Parallel Opportunities**: 28 tasks marked [P]

---

## Suggested MVP Scope

**Minimum Viable Product** = Setup + Foundational + User Story 1

This delivers:
- User registration and authentication
- Student profile creation with all fields
- Resume upload (PDF, 2MB max)
- Form validation
- Basic viewing of created profile

**Total MVP Tasks**: 40 tasks (T001-T040)
**Estimated MVP Effort**: 2-3 days for experienced developer

After MVP validation, incrementally add User Stories 2-5 based on priority and feedback.

