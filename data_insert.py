import pymongo
import scrape_mars
# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
# Select database
db = client.mars_data
#Empty the collections if they exist:
# db.news.drop()
# db.facts.drop()
# db.weather.drop()
# db.images.drop()
# db.featured.drop()

#Get latest mars news
def scrape():
    news = scrape_mars.mars_news()
    db.news.insert_many(news)
    print("News Uploaded!")
    #Get featured image
    mars_pic = scrape_mars.mars_image()
    db.featured.insert_one(mars_pic)
    print("Feature Image Uploaded!")
    #Get latest weather from Twitter
    weather = scrape_mars.mars_weather()
    db.weather.insert_one(weather)
    print("Weather Uploaded!")
    #Get mars facts table
    facts = scrape_mars.mars_facts()
    db.facts.insert_one(facts)
    print("Facts Uploaded!")
    #Get images of mars hemispheres
    hems = scrape_mars.mars_hemispheres()
    db.images.insert_many(hems)
    print("Hemispheres Uploaded!")
