from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

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
    return render_template("agecalculation.html", birthyear=birthyear)

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
