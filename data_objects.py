

class pops_object:
    def __init__(self, pop_id, name, status, location, amenities, website, photo, details, rating, geojson):
        self.pop_id = pop_id
        self.name = name
        self.status = status
        self.location = location
        self.amenities = amenities
        self.website = website
        self.photo = photo
        self.details = details
        self.rating = rating
        self.geojson = geojson


class scrape_object:
    def __init__(self, website, photo, rating, details, icon_list):
        self.website = website
        self.photo = photo
        self.rating = rating
        self.details = details
        self.icon_list = icon_list
