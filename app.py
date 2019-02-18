from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import data_insert

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    featured_img = mongo.db.images.find_one()
    weather = mongo.db.weather.find_one()
    return render_template("index.html", weather=weather, featured=featured_img)


@app.route("/scrape")
def scrape():

    mars_db = mongo.db.mars_data
    mars_db = data_insert.scrape()
    # mars_db.update({}, mars_db, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
