# AIzaSyC87f18k0bYsa3vUmptsBxYLlhbn-C8lMk

import requests
import json
import time
class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        w = open('data/teste.json','w')
        w.write(str(places))
        w.close()
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        w = open('data/'+str(place_id)+'.json','w')
        w.write(str(place_details))
        w.close()
        return place_details

        
if __name__ == '__main__':
    api = GooglePlaces("AIzaSyC87f18k0bYsa3vUmptsBxYLlhbn-C8lMk")
    places = api.search_places_by_coordinate("34.398483,-94.39398", "2000", "restaurant")
    fields = ['name', 'formatted_address', 'rating', 'type']
    for place in places:
        details = api.get_place_details(place['place_id'], fields)
    
