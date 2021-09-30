from flask import Flask
from flask_pymongo import PyMongo

app = Flask("__main__")
app.config["MONGO_URI"] = "mongodb+srv://user:1234@cluster0.k95ys.mongodb.net/test?retryWrites=true&w=majority"
app.config["DEBUG"] = True
mongo = PyMongo(app)

db_cal = mongo.db.calendar
db_user = mongo.db.user
db_sticker = mongo.db.sticker