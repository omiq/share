import logging
import sys
import requests
from bs4 import BeautifulSoup
from html_sanitizer import Sanitizer
from collections import Counter
import re
from googlesearch import search
requests.packages.urllib3.disable_warnings() 

# Request headers to pretend to not be a bot
headers = {
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    "Accept-Encoding": "UTF-8",
}

# Our final list will contain the words and how often they appear
word_count = {}

# HTML sanitization
sanitizer = Sanitizer()  # default configuration
s = 0

# Get the article text from the search result
def extract_article_text(url):

    # Send a GET request to the URL
    response = requests.get(url, headers=headers, allow_redirects=False, verify=False)

    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup.get_text()

# Count occurrences of the search phrase in the article text
def count_search_phrase_occurrences(text, search_phrase):
    text = text.lower()
    search_phrase = search_phrase.lower()
    return text.count(search_phrase)

# Get search results directly using API
def get_serps(search_query):
    results = search(search_query, tld="com", num=20, stop=20, pause=2)
    return results


# What to crawl
keyword = ""
search_query = ""
#print(len(sys.argv))
if len(sys.argv) <= 1:
    print("Enter a search phrase to crawl")
    sys.exit()
elif len(sys.argv) == 3:
    search_query = sys.argv[1]
    keyword = sys.argv[2]
else:
    search_query = sys.argv[1]


# Announce intention
print("GETTING SERP - THIS COULD TAKE A WHILE")

# Turn off logging
log_status = logging.getLogger().getEffectiveLevel()
logging.getLogger().setLevel(logging.CRITICAL)

# Get list of URLs
urlcount = 0
urls = get_serps(search_query)

# Retrieve URL list
print("URLs extracted - Analyzing SERP")

# Grab the keywords for each URL
search_phrase_count = 0
for url in urls:
    count = 0
    text = False
    if(re.search("(http.?:\/\/)", url)): text = extract_article_text(url)
    
    if text:
        if keyword != "": search_query = keyword
        count = count_search_phrase_occurrences(text, search_query)
        print(f"Found the phrase {count} times in {url}")
        search_phrase_count += count
        urlcount +=1

# Report
average = search_phrase_count / urlcount
print("=========================")
print(f"Total count: {search_phrase_count}")
print(f"Average occurrences of '{search_query}' in the crawled pages: {average}")
print("=========================")