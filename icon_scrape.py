import json
from bs4 import BeautifulSoup
from pops import *
from pops_scrape import *

html_file = '/Users/gabrielhidalgo/projects/nyc_pops_map/dataset/pops_website.html'
url = 'https://apops.mas.org/wp-content/themes/mas_pops/assets/img/png/amenities/{}'

image_icons = {
    '24-hour': url.format('allday.png'),
    'Seating':url.format('seating.png'),
    'Lighting':url.format('lighting.png'),
    'Escalator':url.format('escalator.png'),
    'Tables':url.format('table.png'),
    'Drinking Fountain':url.format('drinking_fountain.png'),
    'Litter Receptacles':url.format('litter_receptacles.png'),
    'Bicycle Parking':url.format('bicycle_parking.png'),
    'Climate Control':url.format('climate_control.png'),
    'Water Feature':url.format('fountain.png'),
    'Restrooms':url.format('restrooms.png'),
    'Elevator':url.format('elevator.png'),
}

def get_icon_list(url):
    with open(html_file, encoding="utf-8") as f:
        data = f.read()
        soup = BeautifulSoup(data, 'html.parser')
    items = soup.findAll('figure', {'class', "pops-item"})
    icon_dict = {
        pop.find('a')['href']: icon_list(pop)
        for pop in items
    }
    if not icon_dict[url]:
        return '{}'
    return icon_dict[url]

def icon_list(pop):
    return [
        image_icons[icon['title']]
        for icon in pop.findAll('i')
        if icon['title'] in image_icons.keys()
    ]
