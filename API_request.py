import requests
import json
from bs4 import BeautifulSoup
import secrets

######################################################

### Creating Classes

class restaurant:
    def __init__(self, name, cuisine, distance, review_count, rating):
        self.name = name
        self.cuisine = cuisine
        self.distance = distance
        self.review_count = review_count
        self.rating = rating
    
class property:
    def __init__(self, address, sushi=None, pizza=None, indian=None, rent=None):
        self.address = address
        self.sushi = sushi
        self.pizza = pizza
        self.indian = indian
        self.rent = rent

######################################################

### Declaring variables needed later

yelp_url = "https://api.yelp.com/v3/businesses/search"
yelp_header = {"Authorization":'Bearer {}'.format(secrets.API_key)}

address = input('Please enter an address with no puncuation.\nExample: 105 S State St Ann Arbor MI\n')
# address = "630 N Adams St Ypsilanti MI"
restaurants = {}
properties = {}
first_rent_url = "https://www.rentometer.com/analysis/2-bed/"
second_rent_url = "/hVCNjDdB5fs/quickview"

######################################################

### Defining Functions

def make_restaurant(address, category):
    '''
    Takes address and category (cuisine) and returns a new restaurant object of the category closest to address
        queries yelp API using auth in secrets.py
        restaurant object includes name, category, distance, review_count, and avg rating
    '''
    yelp_params = {"location":address, "categories":category, "sort_by":"distance"}
    yelp_response = requests.get(yelp_url, yelp_params, headers=yelp_header)
    yelp_data = json.loads(yelp_response.content)   
    restaurant_data = yelp_data['businesses'][0]
    new_restaurant_id = restaurant_data['id']
    new_restaurant = restaurant(name = restaurant_data['name'], cuisine = category, distance = restaurant_data['distance'], review_count = restaurant_data['review_count'], rating = restaurant_data['rating'])
    if new_restaurant_id not in restaurants:
        restaurants[new_restaurant_id]= new_restaurant
    return new_restaurant

def get_rent(address):
    '''
    Takes an address and returns the average rent w/in 1/4 mile. 
        Reformats address to query rentometer.com
        Gets rentometer page for address
        Scrapes avg rent using beautifulsoup
    '''
    address_url_string = address.split()[0]
    for word in address.split()[1:]:
        address_url_string += '-' + word
    rent_url = first_rent_url + address_url_string + second_rent_url
    soup = BeautifulSoup(requests.get(rent_url).text, 'html.parser')
    rent = soup.find('abbr', {'title' : 'Sample Mean'}).contents[0]
    return rent

def make_property(address):
    '''
    Takes an address and returns a new property object
        property includes closes of each (sushi, pizza, indian) restaurant type
        and avg rent w/in 1/4 mile
    Also adds new property to properties dict w/ address as key
    '''
    new_sushi = make_restaurant(address, "sushi")
    new_pizza = make_restaurant(address, "pizza")
    new_indian = make_restaurant(address, "indian")
    new_rent = get_rent(address)

    new_property = property(address, sushi=new_sushi, pizza=new_pizza, indian=new_indian, rent = new_rent)
    properties[address] = new_property

    return new_property

######################################################






