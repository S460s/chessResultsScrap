from bs4 import BeautifulSoup
import requests
import time


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
        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.tag = self.url[len(self.url) - 3: len(self.url)]
        self.touramentUrls = self.set_tournamentUrls()

    def printFirst3(self, url):
        fullUrl = f'https://chess-results.com/{url}'
        html = requests.get(fullUrl).text
        soup = BeautifulSoup(html, 'lxml')
        players = soup.find_all('tr', class_=self.tag)
        print('First 3 players are: ')
        for i in range(3):
            playerInfo = players[i].find_all('td')
            elo = players[i].find('td', class_='CRr').text
            print(f'    Name: {playerInfo[3].text}. ELO: {elo}')

    def printTouraments(self):
        tournaments = self.soup.find_all('tr', class_=self.tag)

        for tournament in tournaments:
            tournament_info = tournament.find_all('td')
            number = tournament_info[0].text
            title = tournament_info[1].text
            last_update = tournament_info[2]
            print(f'{number}) Title: {title}, last update: {last_update.text}')
            print(f"Link: {tournament_info[1].a['href']}")
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
                self.printFirst3(tournament_info[1].a['href'])
                print(
                    f"Link: https://chess-results.com/{tournament_info[1].a['href']}")
                print('----------------------------------------------------')


scrapper = ChessRScraper('https://chess-results.com/fed.aspx?lan=1&fed=LTU')
scrapper.printLastDay()


""" if __name__ == '__main__':
    url = input(
        'Enter a url to a ChessResults tourament page (should be in English).')
    search = input(
        'Do you want all tournaments or the ones from the last day? (all, lastday)')
    time_wait = input('Time deley (in mins)')
    scrapper = ChessRScraper(url)
    while True:
            if search.strip() == 'all':
                scrapper.printTouraments()
            elif search.strip() == 'lastday':
                scrapper.printLastDay()
            print(search)
            print(f'Waiting {time_wait} minutes...')
            time.sleep(int(time_wait) * 60) """
