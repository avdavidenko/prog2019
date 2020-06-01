from bs4 import BeautifulSoup # pip install bs4
from typing import List
import requests # pip install requests
import urllib

def links_from_text(text):
    soup = BeautifulSoup(text)
    content = soup.find("div", {"id": "mw-content-text"})
    
    links = content.find_all("a")
    
    for link in links:
        href = link.get('href', '')

        isfile = False
        isservice = False
        if href.startswith('/wiki'):
            url = urllib.parse.unquote(href)
            if url.startswith('/wiki/Файл:'):
                isfile = True
            if url.startswith('/wiki/Служебная:'):
                isservice = True
            if isfile == False and isservice == False:
                yield url 
            
def shortest_path(from_article: str, to_article: str, n_threads: int) -> List[str]:
    path = []
    path.append(from_article)
    for url in links_from_text(requests.get(from_article).text):
        if url == to_article:
            path.append(to_article)
            break  
    return path


start_url = 'https://ru.wikipedia.org/wiki/Теория струн'
final_url = 'https://ru.wikipedia.org/wiki/Теория_бозонных_струн'
final_url = final_url.replace('https://ru.wikipedia.org', '')

path = shortest_path(start_url, final_url, 0)
print(path)

