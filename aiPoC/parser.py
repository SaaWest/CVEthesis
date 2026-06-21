import requests
from bs4 import BeautifulSoup
# Use this to get the code sections of the POC from the url
def exploitPoC(url):
    url = "https://github.com/deeplook/svglib/issues/229"

    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text("\n")
    mid = len(text) // 2
    #print(text)
    return text[:mid]