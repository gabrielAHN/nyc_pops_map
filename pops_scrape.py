import re

from data_objects import scrape_object
from icon_scrape import get_icon_list
from pops import *

POPS_OPEN_WEBSITE = 'https://apops.mas.org/pops/{}/'
RATING_REGEX =  re.compile(r"\d\.\d+")
BAD_PHOTOS = [
    'https://apops.mas.org/wp-content/uploads/2012/10/1515-Broadway.jpg',
    'https://apops.mas.org/wp-content/uploads/2018/11/placeholder-pops-photo.jpg',
    'https://apops.mas.org/wp-content/uploads/2012/10/1515-Broadway.jpg',
]


def website_scrape(build_number):
    url = POPS_OPEN_WEBSITE.format(build_number)
    response = url_request(url)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        soup = soup.find_all('div', {'id', 'single-pops'})
        photo = get_photo(soup)
        rating = get_rating(soup)
        details = get_details(soup)
        icon_list = get_icon_list(url.lower())
    else:
        url =''
        photo = ''
        rating = ''
        details = ''
        icon_list='{}'
    return scrape_object(website=url, photo=photo, rating=rating, details=details, icon_list=icon_list)


def get_rating(soup):
    rating = [
            re.search(RATING_REGEX, rate.text)
            for rates in soup
            for rate in  rates.find_all(
                'div', {'class',"pops_ratings"})
            if rates.find_all(
                'div', {'class',"pops_ratings"})
            ][0]
    if rating:
        rating = rating.group(0)
        if 4 <= float(rating):
            return 'good'
        elif 2 <= float(rating):
            return 'okay'
        else:
            return 'bad'


def get_photo(soup):
    photo = [
            img.find(
                'figure', {'class', 'gallery-image'}
                ).find('img')['src']
            for img in soup
            ][0]
    if photo in BAD_PHOTOS:
        return ''
    return photo


def get_details(soup):
    details = [
            details.text
            for x in soup
            for y in  x.find_all(
                'div', {'class', "section-entry pops-entry with-image"}
            )
            for details in y.find_all('p')
            if 'by Jerold S. Kayden' not in details.text
            and '\xa0' != details.text
            and 'The profile for this POPS has not ' not in details.text
            and 'Information on this privately owned public space will be provided shortly' not in details.text
    ]
    formated_string = '' 
    if details:
        for detail in details:
            detail = re.sub(r'Further information will be.+', '', detail)
            formated_string += '{}\n'.format(detail)
    return formated_string
