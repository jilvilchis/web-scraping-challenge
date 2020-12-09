from flask import Flask, render_template, redirect, url_for, Markup
#from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars_dict = {}
    mars_dict = db.mars.find_one()
    is_empty=False
    # Find one record of data from the mongo database
    # destination_data = mongo.db.collection.find_one()

    if not bool(mars_dict):
        is_empty = True
        print("Dictionary empty")

    # Return template and data
    return render_template("index.html", mars=mars_dict, is_empty=is_empty)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dict = scrape_mars.scrape()
    #Clean the collectio before we start
    db.mars.drop()
    # Update the Mongo database using update and upsert=True
    db.mars.insert(mars_dict)

    # Redirect back to home page
    return render_template("index.html", mars=mars_dict)


if __name__ == "__main__":
    app.run(debug=True)
