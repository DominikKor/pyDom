from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SECRET_KEY"] = "87aa28f53d12b98ffe7f439aa7eaf268"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://rckkgblinsrymr:37831f40b6effc3344ffb24b2dda03c8760fb0daeb820ce368361ab8d7290edc@ec2-54-165-36-134.compute-1.amazonaws.com:5432/dcu9gh8escihdu"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
