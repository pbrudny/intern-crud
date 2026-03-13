"""Profile forms."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp, ValidationError
from datetime import datetime, timedelta


class ProfileForm(FlaskForm):
    """Student profile form."""
    
    # Required fields
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=1, max=100, message='Name must be between 1 and 100 characters')
    ])
    
    email = StringField('Contact Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120)
    ])
    
    index_number = StringField('Student Index Number', validators=[
        DataRequired(message='Index number is required'),
        Length(min=4, max=50, message='Index number must be at least 4 characters'),
        Regexp(r'^[a-zA-Z0-9]+$', message='Index number must be alphanumeric (letters and numbers only)')
    ])
    
    institution = StringField('Educational Institution', validators=[
        DataRequired(message='Institution is required'),
        Length(min=1, max=200, message='Institution name must be between 1 and 200 characters')
    ])
    
    field_of_study = StringField('Field of Study / Major', validators=[
        DataRequired(message='Field of study is required'),
        Length(min=1, max=200, message='Field of study must be between 1 and 200 characters')
    ])
    
    graduation_date = DateField('Graduation Date', validators=[
        DataRequired(message='Graduation date is required')
    ], format='%Y-%m-%d')
    
    # Optional fields
    work_experience = TextAreaField('Work Experience', validators=[
        Optional(),
        Length(max=5000, message='Work experience must not exceed 5000 characters')
    ])
    
    projects = TextAreaField('Projects', validators=[
        Optional(),
        Length(max=5000, message='Projects description must not exceed 5000 characters')
    ])
    
    linkedin_url = StringField('LinkedIn Profile URL', validators=[
        Optional(),
        Length(max=255, message='LinkedIn URL must not exceed 255 characters')
    ])
    
    availability = StringField('Availability', validators=[
        Optional(),
        Length(max=100, message='Availability must not exceed 100 characters')
    ])
    
    locations = StringField('Preferred Locations', validators=[
        Optional(),
        Length(max=255, message='Locations must not exceed 255 characters')
    ])
    
    resume = FileField('Resume (PDF only, max 2MB)', validators=[
        Optional(),
        FileAllowed(['pdf'], 'Only PDF files are allowed')
    ])
    
    submit = SubmitField('Save Profile')
    
    def validate_graduation_date(self, field):
        """Validate graduation date is within reasonable range."""
        if field.data:
            # Check if date is not more than 10 years in the past
            ten_years_ago = datetime.now().date() - timedelta(days=365*10)
            if field.data < ten_years_ago:
                raise ValidationError('Graduation date cannot be more than 10 years in the past')
            
            # Check if date is not more than 10 years in the future
            ten_years_future = datetime.now().date() + timedelta(days=365*10)
            if field.data > ten_years_future:
                raise ValidationError('Graduation date cannot be more than 10 years in the future')

