""" Scrape the index file in the folder
from bs4 import BeautifulSoup

with open('index.html', 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml')
    course_cards = soup.find_all('div', class_='card')
    for course in course_cards:
        course_name = course.h5.text
        course_price = course.a.text
        print(f'{course_name} costs {course_price.split()[-1]}.')
 """

from bs4 import BeautifulSoup
import requests


class ChessRScraper:
    def set_tournamentUrls(self):
        tournaments = self.soup.find_all('tr', class_=self.tag)
        links = []
        for tournament in tournaments:
            tournament_info = tournament.find_all('td')
            links.append(tournament_info[1].a['href'])
        return links

    def __init__(self, url):
        self.url = url
        self.html = html_text = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.tag = self.url[len(self.url) - 3: len(self.url)]
        self.touramentUrls = self.set_tournamentUrls()

    def printTouraments(self):
        tournaments = self.soup.find_all('tr', class_=self.tag)

        for tournament in tournaments:
            tournament_info = tournament.find_all('td')
            number = tournament_info[0].text
            title = tournament_info[1].text
            last_update = tournament_info[2]
            print(f'{number}) Title: {title}, last update: {last_update.text}')


bul = ChessRScraper('https://chess-results.com/fed.aspx?lan=1&fed=BUL')
