from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from psycopg2 import *
import time
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "87aa28f53d12b98ffe7f439aa7eaf268"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://rckkgblinsrymr:37831f40b6effc3344ffb24b2dda03c8760fb0daeb820ce368361ab8d7290edc@ec2-54-165-36-134.compute-1.amazonaws.com:5432/dcu9gh8escihdu"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Bitte melde dich an um diese Seite zu öffnen"
login_manager.login_message_category = "danger"

Jahr = int(time.strftime("%Y"))
Monat = int(time.strftime("%m"))
Tag = int(time.strftime("%d"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}'"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}'"


class RegistrationForm(FlaskForm):
    username = StringField("Benutzername",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("E-Mail",
                           validators=[DataRequired()])
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
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Diese E-Mail ist schon registriert. Bitte wähle einen andere oder melde dich an.")

class LoginForm(FlaskForm):
    email = StringField("E-Mail",
                           validators=[DataRequired()])
    password = PasswordField("Passwort",
                           validators=[DataRequired()])
    remember = BooleanField("Angemeldet bleiben")
    submit = SubmitField("Einloggen")

@app.route("/")
def redirectindex():
    return redirect(url_for("index"))

@app.route("/index.html/")
def index():
    return render_template("index.html")


@app.route("/age/", methods=["POST", "GET"])
def age():
    global birthyear
    if request.method == "POST":
        birthyear = request.form["birthyear"]
        return redirect(url_for("agecalculation", birthyear=birthyear))
    else:
        return render_template("age.html")

@app.route("/agecalculation/")
def agecalculation():
    birthyearSplitted = birthyear.split("-")
    InputTag = birthyearSplitted[2]
    InputMonat  = birthyearSplitted[1]
    InputJahr = birthyearSplitted[0]
    # remergedBirthyear = f"{splitted_day}/{splitted_month}/{splitted_year}"

    Antwort = None
    AntwortWurdest = "Du wurdest"
    GeburtstagAntwortTeilEins = "Alles Gute zu deinem"
    GeburtstagAntwortTeilZwei = "Geburtstag!"
    AntwortWirst = "Du wirst"
    Geburtstag = "nein"
    GanzeAntwort = None

    Alter = Jahr - int(InputJahr)

    if Alter == 0:
        Alter = "geboren"

    InputJahrAlsInt = int(InputJahr)
    InputMonatAlsInt = int(InputMonat)
    InputTagAlsInt = int(InputTag)

    if InputMonatAlsInt > Monat:
        Antwort = AntwortWirst
        GanzeAntwortEins = f"{Antwort} in diesem Jahr {str(Alter)}. "
        GanzeAntwortZwei = f"Jetzt bist du aber {Alter - 1} Jahre alt."
        GanzeAntwort = f"{GanzeAntwortEins}{GanzeAntwortZwei}"
    elif InputMonatAlsInt < Monat:
        Antwort = AntwortWurdest
        if Alter == "geboren":
            GanzeAntwort = f"{Antwort} in diesem Jahr {str(Alter)}!"
        else:
            GanzeAntwort = f"{Antwort} in diesem Jahr {str(Alter)}."
    else:
        if InputTagAlsInt > Tag:
            Antwort = AntwortWurdest
        else:
            if InputTagAlsInt == Tag:
                Geburtstag = "ja"
                Antwort = GeburtstagAntwortTeilEins
            else:
                Antwort = AntwortWurdest
        if Geburtstag == "ja":
            if (InputJahrAlsInt == Jahr) and (InputMonatAlsInt == Monat) and (InputTagAlsInt == Tag):
                GanzeAntwort = "Alles Gute zur Geburt!"
            else:
                GanzeAntwort = f"{GeburtstagAntwortTeilEins} {Alter} {GeburtstagAntwortTeilZwei}"
        else:
            if Alter == "geboren":
                GanzeAntwort = f"{Antwort} in diesem Jahr {str(Alter)}!"
            else:
                if Antwort == AntwortWirst:
                    GanzeAntwortEins = f"{Antwort} in diesem Jahr {str(Alter)}. "
                    GanzeAntwortZwei =  f"Jetzt bist du aber {Alter - 1} Jahr alt."
                    GanzeAntwort = f"{GanzeAntwortEins}{GanzeAntwortZwei}"
                else:
                    GanzeAntwort = f"{Antwort} in diesem Jahr {str(Alter)}."
    return GanzeAntwort
    #  return render_template("agecalculation.html", birthyear=birthyear)

@app.route("/registrieren.html/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/index.html/")
    form = RegistrationForm(meta={'csrf': False})
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        session["user"] = form.username.data
        flash(f"Account erstellt für {form.username.data}! Du kannst dich nun Einloggen!", "success")
        return redirect("/login.html/")
    return render_template("registrieren.html", form=form)

@app.route("/login.html/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/index.html/")
    form = LoginForm(meta={'csrf': False})
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect("/account.html/")
            else:
                flash("Login nicht erfolgreich. Bitte überprüfe die E-Mail und das Passwort.", "danger")
    return render_template("login.html", form=form)

@app.route("/logout.html/")
@login_required
def logout():
    logout_user()
    return redirect("/index.html/")

@app.route("/account.html/")
@login_required
def account():
    return render_template("account.html")

@app.route("/404.html/")
def page404():
    return render_template("404.html")

@app.route("/about-us.html/")
def aboutus():
    return render_template("about-us.html")

@app.route("/blog.html/")
def blog():
    return render_template("blog.html")

@app.route("/blog-single.html/")
def blogsingle():
    return render_template("bloga-single.html")

@app.route("/contact.html/")
def contact():
    return render_template("contact.html")

@app.route("/portfolio.html/")
def portfolio():
    return render_template("portfolio.html")

@app.route("/services.html/")
def services():
    return render_template("services.html")

@app.route("/app-ads.txt/")
def appads():
    return render_template("app-ads.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=False)
