import time

from pops import *
from selenium import webdriver

driver = webdriver.Chrome('/Users/gabrielhidalgo/projects/nyc_pops_map/chromedriver')


def scrape_google(photo, location):
    if photo:
        return photo
    url = 'https://www.google.com/maps/search/+{0},{1}/@{0},{1},17z'.format(
        location['coordinates'][1], location['coordinates'][0])
    driver.get(url)
    time.sleep(4)
    photo = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[1]/div[1]/button/img')
    tag = photo.get_attribute("outerHTML")
    soup = BeautifulSoup(tag, 'html.parser')
    link = soup.find('img')['src'].replace('amp;', '')
    if link:
        return 'https:{}'.format(link)


def clean_link(link):
    if 'https//' in link:
        link = link.replace('https//', '')
    if 'maps.gstatic.com/tactile/pane/default_geocode-2x.png' in link:
        link = ''
    return link
