from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from appdirectory.models import User, Post


class RegistrationForm(FlaskForm):
    username = StringField("Benutzername",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("E-Mail",
                           validators=[DataRequired(), Email()])
    password = PasswordField("Passwort",
                           validators=[DataRequired()])
    confirm_password = PasswordField("Passwort bestätigen",
                           validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Registrieren")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Dieser Benutzername ist schon vergeben. Bitte wähle einen anderen.")

    def validate_email(self, email):
        email = User.query.filter_by(username=email.data).first()
        if email:
            raise ValidationError("Diese E-Mail ist schon registriert. Bitte wähle einen andere oder melde dich an.")

class LoginForm(FlaskForm):
    email = StringField("E-Mail",
                           validators=[DataRequired(), Email()])
    password = PasswordField("Passwort",
                           validators=[DataRequired()])
    remember = BooleanField("Angemeldet bleiben")
    submit = SubmitField("Einloggen")