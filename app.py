from flask import Flask, redirect, url_for, render_template, request
import time

app = Flask(__name__)

year = int(time.strftime("%Y"))
month = int(time.strftime("%m"))
day = int(time.strftime("%d"))

maxdate = f"{year}-{month}-{day}"

@app.route("/")
def redirectindex():
    return redirect(url_for("index"))

@app.route("/index.html/")
def index():
    return render_template("indexnew.html", maxdate=maxdate)


@app.route("/name/", methods=["POST", "GET"])
def age():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("age.html")


@app.route("/name/<usr>/")
def user(usr):
    """try:
        usr = int(usr)
    except Exception:
        namelenght = len(usr)
        capusr = usr.title()
        return f"<h1>Hello {capusr}!</h1> <br> Fun Fact: Dein Name hat {namelenght} Buchstaben!"
    else:
        alter = 2020 - usr
        return f"Du wirst/wurdest dieses Jahr {alter} Jahre alt!"""
    return f"{usr}"

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

