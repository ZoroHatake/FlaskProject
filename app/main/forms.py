from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, Length, Optional
import sqlalchemy as sa
from flask_babel import _, lazy_gettext as _l
from app import db
from app.models import User


# Formular zum Bearbeiten des Benutzerprofils
class EditProfileForm(FlaskForm):
    # Benutzername (Pflichtfeld)
    username = StringField(_l('Username'), validators=[DataRequired()])
    
    # Beschreibung über den Benutzer (max. 140 Zeichen)
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    
    # Submit-Button
    submit = SubmitField(_l('Submit'))

    # Konstruktor speichert ursprünglichen Username für Vergleich
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    # Validierung: Username darf nicht bereits existieren
    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


# Leeres Formular (z.B. für einfache Aktionen wie Follow/Unfollow)
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


# Formular für neue Posts
class PostForm(FlaskForm):
    # Inhalt des Posts (1–140 Zeichen)
    post = TextAreaField(_l('Say something'), validators=[
        DataRequired(), Length(min=1, max=140)])
    
    submit = SubmitField(_l('Submit'))


# Suchformular (GET-Request ohne CSRF)
class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        # Übergibt Query-Parameter aus URL an das Formular
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        
        # Deaktiviert CSRF, da GET-Anfragen verwendet werden
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        
        super(SearchForm, self).__init__(*args, **kwargs)


# Formular für private Nachrichten
class MessageForm(FlaskForm):
    # Nachrichtentext (1–140 Zeichen)
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=1, max=140)])
    
    submit = SubmitField(_l('Submit'))


# Formular für Tasks (dein eigentlich relevantes Feature)
class TaskForm(FlaskForm):
    # Titel des Tasks (Pflichtfeld, max. 100 Zeichen)
    title = StringField(_l('Title'), validators=[DataRequired(), Length(max=100)])
    
    # Beschreibung optional (max. 500 Zeichen)
    description = TextAreaField(_l('Description'), validators=[Optional(), Length(max=500)])
    
    # Status-Auswahl (Dropdown)
    status = SelectField(_l('Status'), choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], validators=[DataRequired()])
    
    # Priorität-Auswahl (Dropdown)
    priority = SelectField(_l('Priority'), choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], validators=[DataRequired()])
    
    # Fälligkeitsdatum (optional)
    due_date = DateField(_l('Due Date'), format='%Y-%m-%d', validators=[Optional()])
    
    # Submit-Button
    submit = SubmitField(_l('Save'))
