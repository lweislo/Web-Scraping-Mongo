from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


def init_browser():
    # Mac-specific browser init
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def mars_news():
    browser = init_browser()
    # Gather the latest Mars news from NASA
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    # Scrape the page
    soup = BeautifulSoup(browser.html, 'lxml')
    browser.quit()
    headline_list = [] # Store the headlines

    # News articles are in a div tag class list_text
    article = soup.find_all('div', class_='list_text')

    # Loop through returned results
    for item in article:
        list_dict = {}
        # Error handling
        try:
            # Grab the headline
            headline = item.find('a').get_text()
            # Grab the strapline
            strapline = item.find('div', class_='article_teaser_body').get_text()
            # Append to the lists
            if (headline and strapline):
                list_dict['headline'] = headline
                list_dict['strapline'] = strapline
                # Put the headline and strapline in a list
                headline_list.append(list_dict)

            else:
                break
        except ElementDoesNotExist as e:
            print(e)
    return headline_list

def mars_image():
    output_dict = {}
    browser = init_browser()
# Visit the JPL site
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = image_url.split('/spaceimages')[0]
    browser.visit(image_url)

    # Click to expand fancybox and get the full image
    try:
        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(3)
    # Scrape out the image link
        soup2 = BeautifulSoup(browser.html, 'lxml')
        browser.quit()
    except ElementDoesNotExist:
        print("Error with featured image")
        browser.quit()

    try:
        image_tag = soup2.find('img', class_='fancybox-image')
        image_title = soup2.find('div', class_='fancybox-title').text
        image_rel_url = image_tag['src']
    #Put together a functional URL
        featured_image_url = base_url + image_rel_url
        output_dict['img_url'] = featured_image_url
        output_dict['title'] = image_title.split('more info')[0].rstrip()
        output_dict['type'] = 'featured'
        return output_dict

    except ElementDoesNotExist:
        print("Error with featured image")

def mars_weather():
    output_dict = {}
    browser = init_browser()
# Visit the Mars Weather Twitter page
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html

    # Scrape out some tweets
    soup3 = BeautifulSoup(html, 'lxml')
    try:
        tweets = soup3.find_all('div', class_='js-tweet-text-container', limit=10)
        browser.quit()
    except AttributeError:
        print("Error with tweet")
        browser.quit()
    # To get around potential retweets,
    # go through the top 10 tweets and find one that looks like weather
    for item in tweets:
        if item.p.text.split(' ')[0] == 'Sol':
            mars_weather = item.p.text.split('pic.twitter')[0]
            mars_weather = mars_weather.split(',')
            output_dict['date'] = mars_weather[0]
            output_dict['high_temp'] = mars_weather[1].split('high ')[1]
            output_dict['low_temp'] = mars_weather[2].split('low ')[1]
            output_dict['pressure'] = mars_weather[3].split('pressure at ')[1]
            output_dict['daylight'] = mars_weather[4].split('daylight ')[1]
            return output_dict

            # Exit the loop if one is found that looks like weather
            break


def mars_facts():
    output_dict={}
# Visit the Mars Space Facts page
    try:
        facts_url = 'http://space-facts.com/mars/'
        tables = pd.read_html(facts_url)
        df = tables[0]
        df.columns=['Fact','Value']
        facts_table = df.to_html(index=False, header=True)
        output_dict['facts_table'] = facts_table
        return output_dict
    except AttributeError as e:
        print(e)

def mars_hemispheres():
# A blank list for the image name and URLS
    hemisphere_image_urls = []
# Open a browser
    browser = init_browser()
# Get the results from Mars Hemispheres image search and store in results
    h_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = h_url.split('/search')[0]
    # Navigate to the page
    browser.visit(h_url)
# Store the html in the soup
    soup4 = BeautifulSoup(browser.html, 'html.parser')
# Parse out the desired content
    try:
        results = soup4.find_all('div', class_='description')
    except AttributeError as e:
        print(e)

    # Iterate through the soup results and store the information as a list of dictionaries
    for item in results:
        link_dict = {} # A blank temporary dictionary for each iteration
        # Get the URL from the a-tag
        link = base_url + item.find('a')['href']
#         print(link) #debugging
        # Visit each link in the results to get full image information
        browser.visit(link)
#         print('trying page') #debugging
        time.sleep(1)

        #Now scrape the page looking for the jpg image with text 'Sample'

        try:
            soup = BeautifulSoup(browser.html, 'html.parser')
            img_list = soup.find('a', text='Sample')
        # Storing the data in the dictionary
            link_dict['title'] = soup.find('h2', class_='title').text
            link_dict['img_url'] = img_list['href']
            link_dict['type'] = 'hemisphere'
        # Appending dictionary to the list for output
            hemisphere_image_urls.append(link_dict)
        except ElementDoesNotExist:
            print("Error with featured image")

    browser.quit()
    return hemisphere_image_urls
