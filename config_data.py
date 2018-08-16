from urllib.request import urlopen
from bs4 import BeautifulSoup

veturilo = "https://www.veturilo.waw.pl/mapa-stacji/"

page = urlopen(veturilo)

soup = BeautifulSoup(page.read(), 'html.parser')

xml_class_name = "price station_list col-xs-12"

file_station_names = 'station_names.txt'
file_station_localizations = 'station_localizations.txt'

station_names_col = 0
station_localization_col = 4
free_bikes_col = 1
free_space_col = 3

