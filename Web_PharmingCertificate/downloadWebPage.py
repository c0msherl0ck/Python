import requests
from bs4 import BeautifulSoup

webURL = "http://107.174.85.141/cert/"
source_code = requests.get(webURL)
plain_text = source_code.text
soup = BeautifulSoup(plain_text, "lxml")  # much more faster than 'html.parser'
f = open("webpageTxt","w")
f.write(soup.prettify())
f.close()