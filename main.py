from bs4 import BeautifulSoup
import requests
import time
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


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
        print(f'Total number of players: {Fore.BLUE}{len(players)}')
        print(f'First {Fore.BLUE}3{Fore.RESET} players are: ')
        for i in range(min(len(players), 3)):
            name = players[i].find_all('a')[0].text
            elo = players[i].find('td', class_='CRr').text
            print(f'{Fore.GREEN}    Name: {name}. ELO: {elo}')

    def printTouraments(self):
        tournaments = self.soup.find_all('tr', class_=self.tag)

        for tournament in tournaments:
            tournament_info = tournament.find_all('td')
            number = tournament_info[0].text
            title = tournament_info[1].text
            last_update = tournament_info[2]
            print(
                f'{Fore.YELLOW}{number}) Title: {title}, {Fore.BLUE}last update: {last_update.text}{Fore.RESET}')
            self.printFirst3(tournament_info[1].a['href'])
            print(f"{Fore.CYAN}Link: {tournament_info[1].a['href']}")
            print(Fore.WHITE + '----------------------------------------------------')

    def printLastDay(self):
        tournaments = self.soup.find_all('tr', class_=self.tag)

        for tournament in tournaments:
            tournament_info = tournament.find_all('td')
            number = tournament_info[0].text
            title = tournament_info[1].text
            last_update = tournament_info[2].text
            if('Days' not in last_update):
                print(
                    f'{Fore.YELLOW}{number}) Title: {title}, {Fore.BLUE}last update: {last_update}{Fore.RESET}')
                self.printFirst3(tournament_info[1].a['href'])
                print(
                    f"{Fore.CYAN}Link: https://chess-results.com/{tournament_info[1].a['href']}")
                print(Fore.WHITE +
                      '----------------------------------------------------')


def startTouramentScrape():
    tag = input(
        f'Enter federation abbreviation {Fore.BLUE}(e.g. BUL for Bulgaria){Fore.RESET}: ')
    search = input(
        f'Do you want all tournaments or the ones from the last day?{Fore.BLUE}(all, lastday){Fore.RESET}: ')
    time_wait = input(f'Time deley {Fore.BLUE}(in mins){Fore.RESET}: ')
    scrapper = ChessRScraper(tag)
    while True:
        if search.strip() == 'all':
            scrapper.printTouraments()
        elif search.strip() == 'lastday':
            scrapper.printLastDay()
        print(search)
        print(f'Waiting {Fore.RED}{time_wait}{Fore.RESET} minutes...')
        time.sleep(int(time_wait) * 60)


class FindPlayer:
    def __init__(self, name):
        self.name = name

    def look_into_tourament(self, url, tag, title):
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        players = soup.find_all('tr', class_=['CRg1', 'CRg2'])
        for player in players:
            if player.find_all('a')[0].text.strip() == self.name.strip():
                print(Fore.WHITE +
                      '----------------------------------------------------')
                print(f'{self.name} has played or is playing in {title}.')
                print(f'Link: {url}')

    def look_for_player(self, tag):
        fullUrl = f'https://chess-results.com/fed.aspx?lan=1&fed={tag}'
        html = requests.get(fullUrl).text
        soup = BeautifulSoup(html, 'lxml')
        tournaments = soup.find_all('tr', class_=tag)
        """ Find all touraments """
        for tournament in tournaments:
            tournament_info = tournament.find_all('td')
            title = tournament_info[1].text
            self.look_into_tourament(
                f"https://chess-results.com/{tournament_info[1].a['href']}", tag, title)


""" 
playerSearch = FindPlayer('Georgiev Konstantin')
playerSearch.look_for_player('BUL') """


if __name__ == '__main__':
    startTouramentScrape()
