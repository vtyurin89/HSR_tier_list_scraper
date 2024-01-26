import requests
import csv
import json
import time
from bs4 import BeautifulSoup

from models import Character

URL = 'https://www.prydwen.gg/star-rail/tier-list/'
URL_ROOT = 'https://www.prydwen.gg'
CHARACTER_URL_FIRST_PART = '/star-rail/characters/'

characters = {}


class HSRParser:
    """
    This class was designed for website prydwen.gg.
    """
    def __init__(self, url: str, character_url_first_part: str):
        self.characters = {}
        self.url = url
        self.character_url_first_part = character_url_first_part

    @staticmethod
    def _calculate_time_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"CHECKING TIME: Process finished in: {end_time - start_time}")
            return result
        return wrapper

    @_calculate_time_decorator
    def get_names_and_urls(self) -> None:
        soup = BeautifulSoup(requests.get(url=self.url).text, 'lxml')
        character_divs = soup.findAll("div", class_='avatar-card card')
        for character_div in character_divs:
            character_url = URL_ROOT + character_div.find('a').attrs.get('href')
            character_name = character_url.split(CHARACTER_URL_FIRST_PART)[1]
            self._create_character(character_name, character_url)
            self._parse_individual_character(character_url, character_name)

    def _create_character(self, character_name: str, character_url: str) -> None:
        self.characters.setdefault(character_name, Character(
            url=character_url,
        ))

    def _get_relics(self, items_div) -> list:
        """
        Find the names of all relics in the div element and add them to the list.
        """
        result = []
        for item in items_div:
            if item.find('div', class_='split-sets row'):
                buttons = item.findAll('button', class_='accordion-button collapsed')
                relic_set = " + ".join([item.find_next('div').next_sibling.strip() for item in buttons])
                result.append(relic_set)
            else:
                relic_set = item.find('button', class_='accordion-button collapsed').\
                    find_next('div').next_sibling.strip()
                result.append(relic_set)
        return result

    @staticmethod
    def _get_best_stats(soup) -> dict:
        stats_divs = soup.find('div', class_='main-stats').findAll('div', class_="col")
        return {item.find('div', class_="stats-header").text.strip():
                [stat.text for stat in item.findAll('div', class_='hsr-stat')]
                for item in stats_divs}

    def _parse_individual_character(self, character_url: str, character_name: str) -> None:
        soup = BeautifulSoup(requests.get(url=character_url).text, 'lxml')
        self.characters[character_name].real_name = soup.find('div', class_='character-top').find('strong').text
        self.characters[character_name].element = soup.find('div', class_='character-top').\
            find('strong').attrs.get('class')[0]
        relic_divs = soup.find('div', class_='relics row row-cols-xxl-2 row-cols-xl-2 row-cols-1').\
            findChildren('div', class_='col')
        relic_items_div = relic_divs[0].findAll("div", class_='relic-sets-rec')
        planetary_items_div = relic_divs[1].findAll("div", class_='relic-sets-rec')
        self.characters[character_name].best_relic_sets = self._get_relics(relic_items_div)
        self.characters[character_name].best_planetary_sets = self._get_relics(planetary_items_div)
        self.characters[character_name].best_stats = self._get_best_stats(soup)



def create_csv():
    pass


def write_csv():
    pass


if __name__ == "__main__":
    my_parser = HSRParser(URL, CHARACTER_URL_FIRST_PART)
    my_parser.get_names_and_urls()
    print(my_parser.characters)


