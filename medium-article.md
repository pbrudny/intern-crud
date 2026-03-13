# Building a Real-World Application with Spec-Driven Development: From Idea to MVP in Hours

## Why Another CRUD App? Because Real Problems Deserve Real Solutions

When I decided to explore spec-driven development, I could have built yet another TODO app. We've all seen them—the "Hello World" of web development tutorials. But here's the thing: I work with students looking for internships, and I saw a real problem that needed solving.

Students struggle to showcase their profiles to potential employers. Companies struggle to find qualified interns. Why not build something that actually solves this problem while learning a new development methodology?

Enter **Speckit**: a specification-driven development framework that promised to transform how we build software. Instead of diving straight into code, I decided to start with a proper specification. Here's how it went.

## The Journey: From Vague Idea to Working MVP

### Step 1: Starting with a Simple Prompt

My initial prompt was straightforward:

> "I want to create a simple CRUD web application in Python 3.14 where students can create their intern profiles. The profile should include basic information like name, email, education details, and optionally work experience and projects. Companies should be able to view these profiles."

That's it. No technical specifications. No database schemas. No wireframes. Just a problem statement.

### Step 2: The Specification Phase

This is where Speckit shined. Instead of jumping into code, the system asked me clarifying questions:

**Question 1**: "Should student phone numbers be collected?"
- My answer: No, but I need student index numbers instead.

**Question 2**: "What format should the student index number have?"
- My answer: Alphanumeric with a minimum of 4 characters.

**Question 3**: "What file types and size limits for resume uploads?"
- My answer: PDF only, maximum 2MB.

**Question 4**: "Who should be able to view profiles?"
- My answer: Authenticated users only (requires login).

**Question 5**: "Who can edit or delete profiles?"
- My answer: Profile owners and administrators.

**Question 6**: "How should administrators be identified?"
- My answer: First user becomes admin, can promote others.

Each question refined the specification. Each answer prevented future bugs and confusion. By the end of this phase, I had a crystal-clear picture of what I was building.

### Step 3: The Planning Phase

With the specification complete, Speckit generated:

1. **Technical Research Document** - Decisions on Flask, SQLAlchemy, Bootstrap 5, UV package manager
2. **Data Model** - Two entities (User, StudentProfile) with proper relationships
3. **API Contracts** - 15 HTTP routes across 4 blueprints
4. **Implementation Plan** - 90 tasks organized by user story

The plan broke down the work into phases:
- **Phase 1**: Setup (14 tasks)
- **Phase 2**: Foundational infrastructure (17 tasks)
- **Phase 3-7**: User stories (41 tasks)
- **Phase 8**: Polish (18 tasks)

### Step 4: Implementation

Here's where it gets interesting. I asked for the MVP only—authentication plus profile creation. That's 40 tasks out of 90.

The implementation was systematic:

**Phase 1: Setup** ✅
- Project structure created
- Dependencies installed with UV (modern Python package manager)
- Configuration files ready
- Bootstrap 5 templates set up

**Phase 2: Foundational** ✅
- Database models (User, StudentProfile)
- Flask-Migrate for database migrations
- Authentication system with Flask-Login
- First user auto-promoted to admin
- Permission utilities

**Phase 3: Profile Creation** ✅
- Comprehensive profile form
- PDF resume upload (validated, 2MB max)
- Form validation (index number, dates, etc.)
- Secure file handling
- Responsive UI

## What I Got: A Working MVP in Record Time

After just a few hours, I had:

✅ **User Registration & Authentication**
- Email-based registration
- Secure password hashing (PBKDF2)
- First user automatically becomes administrator
- Session management with "Remember Me"

✅ **Student Profile Creation**
- Required fields: Name, Email, Index Number, Institution, Field of Study, Graduation Date
- Optional fields: Work Experience, Projects, LinkedIn, Availability, Locations, Resume
- PDF resume upload with validation
- One profile per user

✅ **Security Built-In**
- CSRF protection on all forms
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (Jinja2 auto-escaping)
- File upload validation
- Secure session cookies

✅ **Professional UI**
- Responsive Bootstrap 5 design
- Mobile-friendly navigation
- Flash messages for user feedback
- Form validation with inline errors

## The Numbers

- **Total Tasks**: 90 planned, 40 completed for MVP
- **Time to MVP**: A few hours (vs. days or weeks traditionally)
- **Lines of Code**: ~3,000+
- **Files Created**: 50+
- **Git Commits**: 7 well-organized commits
- **Documentation**: Complete specs, data models, API contracts, quickstart guide

## What Made This Different?

### 1. Specification First, Code Second

Traditional approach:
```
Idea → Code → Debug → Realize you built the wrong thing → Refactor → Repeat
```

Spec-driven approach:
```
Idea → Clarify → Specify → Plan → Implement → Done
```

### 2. Questions Before Assumptions

Instead of assuming what users need, the system asked. Each question prevented:
- Feature creep
- Security vulnerabilities
- UX confusion
- Technical debt

### 3. Incremental Delivery

The task breakdown made it clear what the MVP was (40 tasks) vs. nice-to-haves (50 tasks). I could ship value immediately and iterate based on feedback.

### 4. Documentation as a Byproduct

I didn't write documentation separately. The specification process generated:
- Feature specifications
- Technical decisions document
- Data model documentation
- API contracts
- Quickstart guide
- Task breakdown

All of this came from answering questions and making decisions, not from tedious documentation work.

## Lessons Learned

### 1. Real Problems Are More Motivating

Building a TODO app teaches syntax. Building something you'll actually use teaches software engineering. I now have a tool I can deploy for students I work with.

### 2. Specifications Save Time

The 30 minutes spent answering clarifying questions saved hours of refactoring. Every question prevented a future "Oh, I didn't think about that" moment.

### 3. Modern Tools Matter

Using UV instead of pip, Bootstrap 5 instead of custom CSS, Flask-Login instead of rolling my own auth—these decisions were documented in the research phase and saved countless hours.

### 4. MVP Doesn't Mean Minimum Quality

My MVP has:
- Proper authentication
- Security best practices
- Responsive design
- Form validation
- Error handling
- Professional UI

It's production-ready, not a prototype.

## What's Next?

The remaining 50 tasks are clearly defined:
- **User Story 2**: Profile viewing and browsing (8 tasks)
- **User Story 3**: Profile updates (8 tasks)
- **User Story 4**: Profile deletion (7 tasks)
- **User Story 5**: Administrator management (9 tasks)
- **Polish**: Cross-cutting improvements (18 tasks)

Each user story is independent and can be implemented when needed, based on user feedback.

## Try It Yourself

The complete project is open source:
- **Repository**: [github.com/pbrudny/intern-crud](https://github.com/pbrudny/intern-crud)
- **Pull Request**: [MVP Implementation](https://github.com/pbrudny/intern-crud/pull/1)

Clone it, run it, see spec-driven development in action:

```bash
git clone git@github.com:pbrudny/intern-crud.git
cd intern-crud
uv sync
cd backend
uv run flask run
```

Visit `http://localhost:5000` and you'll see a fully functional application.

## Final Thoughts

Spec-driven development isn't just about tools or frameworks. It's about asking the right questions before writing code. It's about documenting decisions as you make them. It's about building what users need, not what you assume they need.

Would I use this approach again? Absolutely. 

Would I recommend it for your next project? If you're tired of building the wrong thing, refactoring endlessly, or maintaining undocumented code—yes, give it a try.

Sometimes the best way to move fast is to think first, then code.

---

**About the Author**: I'm a developer who works with students seeking internships. This project started as an experiment with spec-driven development and became a tool I'll actually deploy. You can find the complete source code and documentation at [github.com/pbrudny/intern-crud](https://github.com/pbrudny/intern-crud).

**Tech Stack**: Python 3.14, Flask, SQLAlchemy, Bootstrap 5, UV package manager, Speckit framework

**Time to MVP**: A few hours from idea to working application

**Would I do it again?** In a heartbeat.

---

## Appendix: Technical Deep Dive

For those interested in the technical details, here's what the spec-driven process generated:

### The Specification Document

The final specification included:
- 5 user stories with acceptance criteria
- 16 functional requirements
- Security requirements
- Validation rules
- Success criteria

Example functional requirement:
```
FR-008b: System MUST automatically grant administrator role to the
first user who registers in the system
```

This single requirement prevented hours of debate about "How do we bootstrap admin access?"

### The Data Model

Two clean entities with proper relationships:

```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-one relationship
    profile = db.relationship('StudentProfile', backref='user',
                            uselist=False, cascade='all, delete-orphan')

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                       unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    # ... 14 more fields with proper validation
```

### The Task Breakdown

Each task was specific and actionable:

```
- [X] T001 Create project directory structure
- [X] T002 Initialize pyproject.toml with dependencies
- [X] T016 Create User model with authentication
- [X] T024 Implement register route with first-user auto-admin
- [X] T033 Create ProfileForm with validation
- [X] T036 Add file upload validation (PDF, 2MB max)
```

No vague "implement authentication" tasks. Each task had a clear deliverable.

### The Security Checklist

Generated automatically from the specification:

```
✅ Password hashing (Werkzeug PBKDF2)
✅ CSRF protection (Flask-WTF)
✅ SQL injection prevention (SQLAlchemy ORM)
✅ XSS prevention (Jinja2 auto-escaping)
✅ File upload validation (type, size, sanitization)
✅ Secure session cookies (HTTPOnly flag)
✅ Authentication required for profile creation
```

Every security requirement traced back to a specification decision.

### The Modern Python Stack

The research phase documented why each technology was chosen:

**UV over pip**: 10-100x faster, better dependency resolution
**Flask over Django**: Lightweight, appropriate for CRUD
**SQLAlchemy**: Industry-standard ORM, database-agnostic
**Bootstrap 5**: Responsive design out of the box
**pytest**: Modern testing framework

These weren't arbitrary choices—each had documented rationale and alternatives considered.

---

## The Real Win: Confidence

The biggest benefit wasn't speed or code quality (though both were excellent). It was **confidence**.

At every stage, I knew:
- ✅ What I was building (specification)
- ✅ Why I was building it (user stories)
- ✅ How to build it (technical plan)
- ✅ When I was done (acceptance criteria)

No guesswork. No "I think this is what they want." No "I hope this is secure."

Just clear requirements, clear implementation, clear validation.

That's the power of spec-driven development.

---

**Ready to try it yourself?** Start with a real problem, not a tutorial. Ask clarifying questions before writing code. Document decisions as you make them. Build what users need, not what you assume they need.

Your future self (and your users) will thank you.

