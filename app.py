from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

Jahr = 2020
Monat = 4
Tag = 26

@app.route("/")
def redirectindex():
    return redirect(url_for("index"))

@app.route("/index.html/")
def index():
    return render_template("indexnew.html")


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
    #return render_template("agecalculation.html", birthyear=birthyear)

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
    return render_template("blog-single.html")

@app.route("/contact.html/")
def contact():
    return render_template("contact.html")

@app.route("/portfolio.html/")
def portfolio():
    return render_template("portfolio.html")

@app.route("/services.html/")
def services():
    return render_template("services.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run()
