# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 

    #Windows Users
    executable_path = {'executable_path': '/Users/irais/OneDrive/Desktop//Homework/web-scraping-challenge/Mission_to_Mars/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

mars_info = {}

# NASA Mars News
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()


        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        news_html = browser.html

        # Parse with Beautiful Soup
        news_soup = BeautifulSoup(news_html, 'html.parser')


        news_title = news_soup.find('li', class_='slide').find('div', class_='content_title').text
        news_p = news_soup.find('li', class_='slide').find('div', class_='article_teaser_body').text

        # Dictionary entry
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p
        
        return mars_info

    finally:

        browser.quit()

# JPL Mars Space Images - Featured Image
def scrape_mars_image():

    try: 

        # Initialize browser 
        browser = init_browser()
        
        #URL
        image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(image_url)

        #HTML object
        image_html = browser.html

        image_soup = BeautifulSoup(image_html, 'html.parser')

        
        image = image_soup.find(class_='button fancybox')['data-fancybox-href']
        featured_image_url = 'https://www.jpl.nasa.gov/'+ image

        # Dictionary entry
        mars_info['featured_image_url'] = featured_image_url 
        
        return mars_info
    
    finally:

        browser.quit()

        

# Mars Weather 
def scrape_mars_weather():

    try: 

        # Initialize browser 
        browser = init_browser()

        # URL

        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        # HTML object
        weather_html = browser.html

        weather_soup = BeautifulSoup(weather_html, 'html.parser')
                
        # Finding and storing Tweet text

        mars_weather = weather_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
        mars_weather = mars_weather.split('pic')[0]
        
        # Dictionary entry 
        mars_info['mars_weather'] = mars_weather
        
        return mars_info
   
    finally:

        browser.quit()


# Mars Facts
def scrape_mars_facts():
    

    # URL
    marsfacts_url = 'https://space-facts.com/mars/'
    
    # Using Pandas to read and get table

    marsfacts_table = pd.read_html(marsfacts_url)
    marsfacts_df = pd.DataFrame(marsfacts_table[0])

    #Assign Column Names
    marsfacts_df.columns = ['Fact','Value']

    marsfacts_df = marsfacts_df.set_index('Fact')
    marsfacts_df  

    # Use to_html method to generate HTML tables
    marsfacts_html = marsfacts_df.to_html(header=True, index=True)
    
    # Dictionary entry
    mars_info['mars_facts'] = marsfacts_html

    return mars_info


# Mars Hemispheres



def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # url for hemisphers
        hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hem_url)

        # HTML Object
        hem_html = browser.html

        hem_soup = BeautifulSoup(hem_html, 'html.parser')

        # Retreive 
        results = hem_soup.find_all('div', class_='item')

        # Create a list
        hemisphere_image_urls = []
        # hiu = []

        # Store the main_ul 
        base_url = 'https://astrogeology.usgs.gov' 
        # hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items previously stored
        for x in results: 
            # Store title
            title = x.find('h3').text
            
            # Store link that leads to full image website
            partial_img_url = x.find('a', class_='itemLink product-item')['href']
            
            # Visit the link that contains the full image website 
            browser.visit(base_url + partial_img_url)
            
            # HTML Object of individual hemisphere information website 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image source 
            img_url = base_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        mars_info['hemisphere_image_urls'] = hemisphere_image_urls

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()


# def scrape_mars_hemispheres():

#     try: 
#         # Initialize browser 
#         browser = init_browser()

#         # URL
#         hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#         browser.visit(hem_url)

#         # HTML object
#         hem_html = browser.html

#         hem_soup = BeautifulSoup(hem_html, 'html.parser')
    
#        # Create a for loop to click on each hemisphere phto and store in a dictionary


#          # Empty list to store results
#         hemisphere_image_urls = []

#         # Content wrapping links and info for each hemisphere
#         results = hem_soup.find_all('div', class_='item')

#         # Base URL

#         base_url = 'https://astrogeology.usgs.gov/'

#         # Loop through results

#         for x in results:
            
#             title = x.find('h3').text
            
#             image_url = x.find('a', class_='itemLink product-item')['href']
            
#             browser.visit(base_url+image_url)
            
#             hem2_html = browser.html
            
#             hem2_soup = BeautifulSoup(hem2_html, 'html.parser')
            
#             img_url = base_url + hem2_soup.find('img', class_='wide-image')['src']
            
#             hemisphere_image_urls.append({'title' : title, 'img_url' : img_url}) 
              
#         mars_info['hem_urls'] = hemisphere_image_urls

        
#         # Return dictionary 

#         return mars_info
#     finally:

#         browser.quit()