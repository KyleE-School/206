import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET

serviceurl = 'http://maps.googleapis.com/maps/api/geocode/xml?'

while True:
    address = input('Enter location: ')
    if len(address) < 1: break

    url = serviceurl + urllib.parse.urlencode({'address': address})
    print('Retrieving', url)
    uh = urllib.request.urlopen(url)
    data = uh.read()
    # print('Retrieved', len(data), 'characters')
    # print(data.decode())
    tree = ET.fromstring(data)

    results = tree.findall('result')
    # lat = results[0].find('geometry').find('location').find('lat').text
    # lng = results[0].find('geometry').find('location').find('lng').text
    # location = results[0].find('formatted_address').text

    # print('lat', lat, 'lng', lng)
    # print(location)

    place = results[0].findall('address_component')
    # print("length of place is ", len(place))
    # print("type of place is ", type(place))
    for p in place:
        for attr in p:
            if attr.text == "country":
                print(p.find('short_name').text)
