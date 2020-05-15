from flask import redirect, url_for, render_template, flash, request, session
from flask_login import login_user, current_user, logout_user, login_required, login_manager, LoginManager
from appdirectory.models import User, Post
from appdirectory.forms import RegistrationForm, LoginForm
from appdirectory import app, db, bcrypt
import time

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Bitte melde dich an, um diese Seite zu öffnen"
login_manager.login_message_category = "danger"

Jahr = int(time.strftime("%Y"))
Monat = int(time.strftime("%m"))
Tag = int(time.strftime("%d"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return redirect(url_for("index"))

@app.route("/index.html/")
def index():
    sitename = "Home"
    return render_template("index.html", title=sitename, sitename=sitename)

@app.route("/test/")
def testsite():
    sitename = "Testseite"
    return render_template("testsite.html", title=sitename, sitename=sitename)


@app.route("/alter.html/", methods=["POST", "GET"])
def age():
    sitename = "Alter berechnen"
    global birthyear
    if request.method == "POST":
        birthyear = request.form["birthyear"]
        return redirect(url_for("agecalculation", birthyear=birthyear))
    else:
        return render_template("age.html", title=sitename, sitename=sitename)

@app.route("/alter-berechnen/")
def agecalculation():
    sitename = "Berechnung"
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
    return render_template("agecalculation.html", GanzeAntwort=GanzeAntwort, title=sitename, sitename=sitename)

@app.route("/registrieren/", methods=["GET", "POST"])
def register():
    sitename = "Registrieren"
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm(meta={'csrf': False})
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        session["user"] = form.username.data
        flash(f"Account erstellt für {form.username.data}! Du kannst dich nun Einloggen!", "success")
        return redirect(url_for("login"))
    return render_template("registrieren.html", form=form, title=sitename, sitename=sitename)

@app.route("/login/", methods=["GET", "POST"])
def login():
    sitename = "Einloggen"
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm(meta={'csrf': False})
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("account"))
            else:
                flash("Login nicht erfolgreich. Bitte überprüfe die E-Mail und das Passwort.", "danger")
    return render_template("login.html", form=form, title=sitename, sitename=sitename)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/account.html/")
@login_required
def account():
    sitename = "Account"
    return render_template("account.html", title=sitename, sitename=sitename)

@app.route("/über-uns.html/")
def about_us():
    sitename = "Über uns"
    return render_template("about-us.html", title=sitename, sitename=sitename)

@app.route("/blog.html/")
def blog():
    sitename = "Blog"
    return render_template("blog.html", title=sitename, sitename=sitename)

@app.route("/einzelblog.html/")
def blog_single():
    sitename = "Einzelblog"
    return render_template("blog-single.html", title=sitename, sitename=sitename)

@app.route("/kontakt.html/")
def contact():
    sitename = "Kontakt"
    return render_template("contact.html", title=sitename, sitename=sitename)

@app.route("/portfolio.html/")
def portfolio():
    sitename = "Portfolio"
    return render_template("portfolio.html", title=sitename, sitename=sitename)

@app.route("/services.html/")
def services():
    sitename = "Service"
    return render_template("services.html", title=sitename, sitename=sitename)

@app.route("/app-ads.txt/")
def appads():
    return render_template("app-ads.html")

@app.route("/404.html/")
def error_404_page():
    sitename = "404"
    return render_template("404.html", title=sitename, sitename=sitename)

@app.errorhandler(404)
def not_found(e):
    return redirect(url_for("error_404_page"))
