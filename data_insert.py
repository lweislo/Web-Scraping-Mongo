import pymongo
import scrape_mars
# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
# Select database
db = client.mars_data
#Empty the collections if they exist:
db.news.drop()
db.facts.drop()
db.weather.drop()
db.images.drop()
db.featured.drop()

#Get latest mars news
def scrape():
    news = scrape_mars.mars_news()
    try:
        db.news.insert_many(news)
        print("News Uploaded!")
    except TypeError as e:
        print("Mars News Error" + e)
    #Get featured image
    mars_pic = scrape_mars.mars_image()
    try:
        db.featured.insert_one(mars_pic)
        print("Feature Image Uploaded!")
    except TypeError as e:
        print("Feature Image Error" + e)
    #Get latest weather from Twitter
    weather = scrape_mars.mars_weather()

    try:
        db.weather.insert_one(weather)
        print("Weather Uploaded!")
    # Get mars facts table
    except TypeError as e:
        print("Weather Tweet Error" + e)

    facts = scrape_mars.mars_facts()
    try:
        db.facts.insert_one(facts)
        print("Facts Uploaded!")
        # Get images of mars hemispheres
    except TypeError as e:
        print("Mars Facts Error" + e)

    hems = scrape_mars.mars_hemispheres()
    try:
        db.images.insert_many(hems)
        print("Hemispheres Uploaded!")
    except TypeError as e:
        print("Hemisphere scrape error" + e)
