import requests
import json
import secrets

def get_cache(file):
    try:
        cache_file = open(file, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(dictionary, file):
    cache_file = open(file, 'w')
    contents_to_write = json.dumps(dictionary)
    cache_file.write(contents_to_write)
    cache_file.close()

def get_restaurants(address, category):
    '''
    Takes address and category (cuisine) and returns a new restaurant object of the category closest to address
        queries yelp API using auth in secrets.py
        restaurant object includes name, category, distance, review_count, and avg rating
    '''
    address_cache = get_cache('address_cache.txt')
    if address not in address_cache:
        yelp_url = "https://api.yelp.com/v3/businesses/search"
        yelp_header = {"Authorization":'Bearer {}'.format(secrets.yelp_key)}
        yelp_params = {"location":address, "categories":category, "sort_by":"distance"}
        response = requests.get(yelp_url, yelp_params, headers=yelp_header)

    try:
        yelp_data = json.loads(response.content)   
        restaurant_data = yelp_data['businesses'][0]
        new_restaurant_dict = {'name':restaurant_data['name'],'distance':int(restaurant_data['distance']),'review_count':restaurant_data['review_count'],'rating':restaurant_data['rating']}
    except:
        new_restaurant_dict = {'name':'unknown', 'distance':'unknown', 'review_count':'unknown', 'rating':'unknown'}
    address_cache[address] = new_restaurant_dict
    save_cache(address_cache, 'address_cache.txt')
    return new_restaurant_dict

def geolocate(address):
    '''
    Takes address, queries census.gov geocoder API, and returns dict with address info
    '''
    url = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress"
    params = {"address":address, "vintage":"ACS2021_Current", "benchmark":"Public_AR_Current", "format":"json"}
    response = requests.get(url, params)
    if response.status_code == 200:
        json_data = json.loads(response.content)
    else: json_data = None
    return json_data

def get_location(address):
    '''
    Geolocates address with geolocate() helper
    Then pulls out relevant (state and tract) info to return as dict
    '''
    location_data = geolocate(address)
    try: # if geolocate was successful
        state = location_data['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['STATE']
        tract = location_data['result']['addressMatches'][0]['geographies']['Census Tracts'][0]['TRACT']
        location_dict = {'state':state, 'tract':tract}
        return location_dict
    except: # if geolocate unsuccessful, return None
        return None

def make_rent_dict(data):
    '''
    helper func for get_rent
    turns list of lists into dict with key = tract num and val dict avg. rent:value
    '''
    dict = {}
    for x in data[1:]: # ignore header row
        dict[int(x[4])] = {'rent':x[1]} # create dict w/ relevant info from list of lists
    return dict

def get_rent(address):
    '''
    returns average rent per US Census 2019 ACS5 for census tract of given address
    '''
    location_dict = get_location(address)
    rent_cache = get_cache('census_cache.txt')
    if location_dict is None:
        return 'unknown'
    state = location_dict['state']
    tract = location_dict['tract']
    if location_dict['state'] not in rent_cache: 
        print('getting MI state info...')  
        response = requests.get(f'https://api.census.gov/data/2019/acs/acs5/profile?get=NAME,DP04_0134E&for=tract:*&in=state:{state}&key={secrets.census_key}')
        data = response.json()
        rent_cache[state] = make_rent_dict(data)
        save_cache(rent_cache, 'census_cache.txt')
    try:    
        rent = rent_cache[state][tract]['rent']
    except: 
        rent = 'unknown'
    return rent

def new_property(address):
    '''
    Takes an address and returns a dict w/ info on:
        closest of each (sushi, pizza, indian) restaurant type
        and avg rent in census tract of address
    '''
    new_property = {}
    new_property['sushi'] = get_restaurants(address, "sushi")
    new_property['pizza'] = get_restaurants(address, "pizza")
    new_property['indian'] = get_restaurants(address, "indian")
    new_property['rent'] = get_rent(address)

    return new_property
    

def cache_setup(): 
    '''
    setup cache to ensure there are addresses available for analysis
    '''
    properties = get_cache('address_cache.txt')
    if len(properties) < 1:
        print('One moment, loading cache...')
        with open('mich_addresses.txt', 'r') as file:
            mich_addresses = file.read() # load in 100 random Michigan addresses to build cache
        for address in mich_addresses:
            if address not in properties:    
                properties[address] = new_property(address)

        save_cache(properties, 'address_cache.txt')







