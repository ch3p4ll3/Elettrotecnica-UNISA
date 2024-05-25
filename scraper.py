from bs4 import BeautifulSoup
import requests
from db import Posts
from pony.orm import db_session, ObjectNotFound
from datetime import datetime


class Scraper:
    def __init__(self) -> None:
        self.url = "https://www.elettrotecnica.unisa.it/didattica/did_etbachecaesami"
    
    def scrape(self):
        page = requests.get(self.url, verify=False)

        soup = BeautifulSoup(page.content, "html.parser")

        a = soup.find_all("li", attrs={"class": "pdf"})
        new_elements = []

        for i in a:
            link = i.find("a")
            pdf = link.attrs['href']
            title = link.text
            
            new_elements.extend(self.__update_database(pdf, title))

        return new_elements

    def __update_database(self, url, title):
        new_elements = []

        with db_session:
            post = Posts.get(id=title)

            if post is None:
                post = Posts(id=title, url=url)
                new_elements.append(post)

        return new_elements
