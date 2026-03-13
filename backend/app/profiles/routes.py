"""Profile routes."""
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, current_app, abort
from flask_login import login_required, current_user
from app import db
from app.profiles import profiles
from app.profiles.forms import ProfileForm
from app.models.profile import StudentProfile


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_resume(file, user_id):
    """Save uploaded resume file.

    Args:
        file: FileStorage object from form
        user_id: ID of the user uploading the file

    Returns:
        str: Filename of saved file, or None if save failed
    """
    if not file or file.filename == '':
        return None

    if not allowed_file(file.filename):
        return None

    # Check file size (should be handled by Flask config, but double-check)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > current_app.config['MAX_CONTENT_LENGTH']:
        return None

    # Create secure filename with user_id prefix
    original_filename = secure_filename(file.filename)
    timestamp = int(Path(current_app.root_path).stat().st_mtime)
    filename = f"{user_id}_{timestamp}_{original_filename}"

    # Create user-specific upload directory
    upload_dir = Path(current_app.config['UPLOAD_FOLDER']) / str(user_id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    filepath = upload_dir / filename
    file.save(str(filepath))

    return filename


def delete_resume(filename, user_id):
    """Delete resume file.

    Args:
        filename: Name of file to delete
        user_id: ID of the user who owns the file
    """
    if not filename:
        return

    filepath = Path(current_app.config['UPLOAD_FOLDER']) / str(user_id) / filename
    if filepath.exists():
        filepath.unlink()


@profiles.route('/')
@login_required
def list_profiles():
    """List all student profiles."""
    profiles_list = StudentProfile.query.all()

    # Check if current user has a profile
    user_profile = StudentProfile.query.filter_by(user_id=current_user.id).first()

    # For now, redirect to create profile if user doesn't have one
    if not user_profile:
        flash('Welcome! Please create your profile to get started.', 'info')
        return redirect(url_for('profiles.create_profile'))

    # Otherwise show a simple message (full listing to be implemented later)
    flash(f'Welcome back! You have a profile. Full profile listing coming soon.', 'info')
    return redirect(url_for('profiles.view_profile', profile_id=user_profile.id))


@profiles.route('/create', methods=['GET', 'POST'])
@login_required
def create_profile():
    """Create a new student profile."""
    # Check if user already has a profile
    existing_profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if existing_profile:
        flash('You already have a profile. You can edit it instead.', 'warning')
        return redirect(url_for('profiles.view_profile', profile_id=existing_profile.id))

    form = ProfileForm()
    if form.validate_on_submit():
        # Handle resume upload
        resume_filename = None
        if form.resume.data:
            resume_filename = save_resume(form.resume.data, current_user.id)
            if not resume_filename:
                flash('Resume upload failed. Please ensure the file is a PDF and under 2MB.', 'danger')
                return render_template('create.html', form=form)

        # Create profile
        profile = StudentProfile(
            user_id=current_user.id,
            name=form.name.data,
            email=form.email.data,
            index_number=form.index_number.data,
            institution=form.institution.data,
            field_of_study=form.field_of_study.data,
            graduation_date=form.graduation_date.data,
            work_experience=form.work_experience.data,
            projects=form.projects.data,
            linkedin_url=form.linkedin_url.data,
            availability=form.availability.data,
            locations=form.locations.data,
            resume_filename=resume_filename
        )

        db.session.add(profile)
        db.session.commit()

        flash('Your profile has been created successfully!', 'success')
        return redirect(url_for('profiles.view_profile', profile_id=profile.id))

    return render_template('create.html', form=form)


@profiles.route('/<int:profile_id>')
@login_required
def view_profile(profile_id):
    """View a student profile."""
    profile = StudentProfile.query.get_or_404(profile_id)
    return render_template('view.html', profile=profile)

