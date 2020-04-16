from flask import Flask, redirect, url_for, render_template, request


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/welcome/<name>")
def welcome(name):
    name = name.title()
    return f"Hello {name}!"


@app.route("/name/", methods=["POST", "GET"])
def age():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("age.html")

@app.route("/name/<usr>")
def user(usr):
    namelenght = len(usr)
    capusr = usr.title()
    return f"<h1>Hello {capusr}!</h1> <br> Fun Fact: Your name has {namelenght} letters!"

if __name__ == "__main__":
    app.run()
