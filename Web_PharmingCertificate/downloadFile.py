import os
import requests
from bs4 import BeautifulSoup

print(0)
webURL = "http://107.174.85.141/cert/"
# webURL = "http://holywaterkim.tistory.com/"
source_code = requests.get(webURL)
plain_text = source_code.text
print(1)
soup = BeautifulSoup(plain_text, "lxml") # much more faster than 'html.parser'
# print(soup)
print(2)
for link in soup.select("tr > td > a"):
    # parse fileName(same as URL) from a tag
    fileName = link.get('href')
    print(fileName)
    href = webURL + fileName
    # download file from web
    try:
        r = requests.get(href)
        path = "certificate_set/"
        f = open(path + fileName,"wb")
        f.write(r.content)
        f.close()
    except:
        print("error : " + fileName)
print(3)



