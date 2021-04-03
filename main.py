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
            print(f"Link to tournament: {tournament_info[1].a['href']}")
            print('----------------------------------------------------')

    def printLastDay(self):
        tournaments = self.soup.find_all('tr', class_=self.tag)

        for tournament in tournaments:
            tournament_info = tournament.find_all('td')
            number = tournament_info[0].text
            title = tournament_info[1].text
            last_update = tournament_info[2].text
            if('Days' not in last_update):
                print(f'{number}) Title: {title}, last update: {last_update}')
                print(
                    f"Link to tournament: https://chess-results.com/{tournament_info[1].a['href']}")
                print('----------------------------------------------------')


bul = ChessRScraper('https://chess-results.com/fed.aspx?lan=1&fed=BUL')
bul.printLastDay()
