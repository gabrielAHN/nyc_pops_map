import json
import requests

from bs4 import BeautifulSoup
from data_objects import *
from pops_scrape import *
from google_scrape import *


POPS_OPEN_DATA = "https://data.cityofnewyork.us/resource/rvih-nhyn.json"
BBL_GEOJSON = "/Users/gabrielhidalgo/projects/nyc_pops_map/dataset/building_footprints.geojson"


def url_request(url):
    responses = requests.get(url, timeout=10.00)
    if responses:
        return responses


def get_geojson_dict():
    with open(BBL_GEOJSON) as data:
        bbl_geojson = json.load(data)
    geo_dict = {
        building['properties']['base_bbl']:building['geometry']
        for building in bbl_geojson['features']
        if building['geometry']['type'] != 'Point'
    }
    return geo_dict


def geojson_matching(response, geo_dict):
    if 'bbl' in response.keys():
        return json.dumps(geo_dict.get(response['bbl'], '{}'))
    return '{}'


def pop_object(response, geo_dict):
    scraped_object = website_scrape(response['pops_number'])
    geojson = geojson_matching(response, geo_dict)
    photo = scrape_google(scraped_object.photo, response.get('geocoded_column'))
    fact = pops_object(
            pop_id = response.get('pops_number'),
            name = response.get('building_address_with_zip').title(),
            status = response.get('building_constructed'),
            location = response.get('geocoded_column'),
            amenities = scraped_object.icon_list,
            website = scraped_object.website,
            photo = photo,
            details = scraped_object.details,
            rating = scraped_object.rating,
            geojson = geojson
        )
    return fact


def making_json_file(facts):
    rows = []
    for i in range(0, len(facts)):
        fact = {
            "model": "topics.pops_location",
            "pk": i+1,
            "fields": {
                'pop_id': facts[i].pop_id,
                'name': facts[i].name,
                'longitude': facts[i].location['coordinates'][0],
                'latitude': facts[i].location['coordinates'][1],
                'amenities': "{}".format(json.dumps(facts[i].amenities)),
                'website': facts[i].website,
                'geojson': "{}".format(facts[i].geojson),
                'photo': facts[i].photo,
                'rating': facts[i].rating,
                'details': facts[i].details,
            }
        }
        rows.append(fact)
    with open('pops_data.json', 'w') as outfile:
        json.dump(rows, outfile)


def main():
    geo_dict = get_geojson_dict()
    responses = url_request(POPS_OPEN_DATA)
    if responses:
        pops_data = responses.json()
        pop_objects = [
                pop_object(row, geo_dict)
                for row in pops_data
            ]
        making_json_file(pop_objects)


if __name__ == "__main__":
    main()
