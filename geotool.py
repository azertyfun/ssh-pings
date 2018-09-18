import requests
import json

ip_cache = {}

def get_country(origin):
    if origin in ip_cache:
        return ip_cache[origin]

    url = 'http://ip-api.com/json/' + origin
    print('GET ' + url)
    response = requests.get(url)
    if response.status_code != 200:
        print('Error: Could not get country information for origin "' + origin + '" (status code ' + response.status_code + ')')
        return None
    if not 'content-type' in response.headers or response.headers['content-type'].split(';')[0].strip() != 'application/json':
        print('Unknown content-type from ip-api.com')
        print(response.headers['content-type'])
        return None
    
    j = json.loads(response.text)

    info = {
        'lat': j['lat'],
        'lon': j['lon'],
        'country': j['countryCode']
    }

    ip_cache[origin] = info

    return info
