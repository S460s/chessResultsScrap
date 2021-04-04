from bs4 import BeautifulSoup
import requests
import time


class ChessRScraper:
    def __init__(self, tag):
        self.tag = tag
        self.html = requests.get(
            f'https://chess-results.com/fed.aspx?lan=1&fed={self.tag}').text
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.url = f'https://chess-results.com/fed.aspx?lan=1&fed={self.tag}'

    def printFirst3(self, url):
        fullUrl = f'https://chess-results.com/{url}'
        html = requests.get(fullUrl).text
        soup = BeautifulSoup(html, 'lxml')
        players = soup.find_all('tr', class_=['CRg1', 'CRg2'])
        print(f'Total number of players: {len(players)}')
        print('First 3 players are: ')
        for i in range(min(len(players), 3)):
            name = players[i].find_all('a')[0].text
            elo = players[i].find('td', class_='CRr').text
            print(f'    Name: {name}. ELO: {elo}')

    def printTouraments(self):
        tournaments = self.soup.find_all('tr', class_=self.tag)

        for tournament in tournaments:
            tournament_info = tournament.find_all('td')
            number = tournament_info[0].text
            title = tournament_info[1].text
            last_update = tournament_info[2]
            print(f'{number}) Title: {title}, last update: {last_update.text}')
            self.printFirst3(tournament_info[1].a['href'])
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


def startTouramentScrape():
    tag = input('Enter federation abbreviation (e.g. BUL for Bulgaria)')
    search = input(
        'Do you want all tournaments or the ones from the last day? (all, lastday)')
    time_wait = input('Time deley (in mins)')
    scrapper = ChessRScraper(tag)
    while True:
        if search.strip() == 'all':
            scrapper.printTouraments()
        elif search.strip() == 'lastday':
            scrapper.printLastDay()
        print(search)
        print(f'Waiting {time_wait} minutes...')
        time.sleep(int(time_wait) * 60)


class FindPlayer:
    def __init__(self, name):
        self.name = name

    def look_into_tourament(self, url, tag, title):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        players = soup.find_all('tr', class_=['CRg1', 'CRg2'])
        for player in players:
            print(player.find_all('a')[0].text.strip(), self.name.strip())

    def look_for_player(self, tag):
        fullUrl = f'https://chess-results.com/fed.aspx?lan=1&fed={tag}'
        html = requests.get(fullUrl).text
        soup = BeautifulSoup(html, 'lxml')
        tournaments = soup.find_all('tr', class_=tag)
        """ Find all touraments """
        for tournament in [tournaments[0]]:
            tournament_info = tournament.find_all('td')
            title = tournament_info[1].text
            self.look_into_tourament(
                f"https://chess-results.com/{tournament_info[1].a['href']}", tag, title)


""" playerSearch = FindPlayer('Nikolov Momchil')
playerSearch.look_for_player('BUL') """


if __name__ == '__main__':
    startTouramentScrape()
