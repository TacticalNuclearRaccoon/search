import requests
import urllib
#import pandas as pd
#from requests_html import HTML
from requests_html import HTMLSession
from urllib.request import urlopen
from bs4 import BeautifulSoup
from transformers import pipeline


def get_source(url):
	
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)
        

def scrape_google(query):
	query = urllib.parse.quote_plus(query)
	response = get_source("https://www.google.co.uk/search?q=" + query)
	links = list(response.html.absolute_links)
	google_domains = ('https://www.google.', 'https://google.','https://webcache.googleusercontent.','http://webcache.googleusercontent.','https://policies.google.','https://support.google.','https://maps.google.')
	for url in links[:]:
		if url.startswith(google_domains):
			links.remove(url)
	return links
    
    
def text_extractor_html(url):
	html = urlopen(url).read()
	soup = BeautifulSoup(html, features="html.parser")
	# kill all script and style elements
	for script in soup(["script", "style"]):
		script.extract()    # rip it out
	# get text
	text = soup.get_text()
	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	text = '\n'.join(chunk for chunk in chunks if chunk)
	new_text = text.replace('\n','')
	return new_text
    
    
pipe = pipeline("summarization", model="plguillou/t5-base-fr-sum-cnndm")

def generate_summary(in_text):
	'''Genetates an abstractive summary of given text 
	using T5 base french model from hugging face'''
	#print(in_text)
	answer = pipe(in_text, min_length=5, max_length=500)
	print(answer)
	return answer[0]["summary_text"]
  
  
