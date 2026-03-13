"""StudentProfile model for intern candidate information."""
from datetime import datetime, timezone
from app import db


class StudentProfile(db.Model):
    """Student profile model for intern candidates."""
    
    __tablename__ = 'student_profile'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False, index=True)
    
    # Required fields
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    index_number = db.Column(db.String(50), nullable=False)
    institution = db.Column(db.String(200), nullable=False, index=True)
    field_of_study = db.Column(db.String(200), nullable=False, index=True)
    graduation_date = db.Column(db.Date, nullable=False)
    
    # Optional fields
    work_experience = db.Column(db.Text, nullable=True)
    projects = db.Column(db.Text, nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    availability = db.Column(db.String(100), nullable=True)
    locations = db.Column(db.String(255), nullable=True)
    resume_filename = db.Column(db.String(255), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                          onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    def __repr__(self):
        """String representation of StudentProfile."""
        return f'<StudentProfile {self.name} - {self.email}>'

