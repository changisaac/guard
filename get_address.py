# pip install -U googlemaps

import googlemaps
import json

import urllib
import xml.etree.ElementTree as ET

gmaps = googlemaps.Client(key='AIzaSyD_OOP5xcr1h_PhYquy3moSgQW4FFsQueU')
"""
with open('/Users/kberry/Downloads/20200306-175204.json') as f:
  data = json.load(f)

i = 0

print(len(data))
"""

"""
for key, val in data.items():
    # print(key, '->', val)
    if (val["latitude"] and val["longitude"]):
        addresses = gmaps.reverse_geocode((val["latitude"], val["longitude"]))
        # print(val["latitude"], "  ", val["longitude"], "  -->  ")
        j = 0
        for address in addresses:
            # if 'route' in address["types"]:
            print(i, '  ', address["types"], end='\r')
            if 'parking' in address["types"]:
                print(j, "  ", address["formatted_address"])
                print("This is an intersection")
                num_intersections += 1
            j += 1

        i += 1
        # print(i,end='\r')
    if num_intersections > 3 or i > 10000:
        break
"""
def get_addresses(location):
    addresseses = []
    num_parking = 0
    num_intersections = 0
    if (location["latitude"] and location["longitude"]):
        addresses = gmaps.reverse_geocode((location["latitude"], location["longitude"]))
        # print(val["latitude"], "  ", val["longitude"], "  -->  ")
        j = 0
        for address in addresses:
            # if 'route' in address["types"]:
            # print(i, '  ', address["types"])
            if 'parking' in address["types"]:
                print(j, "  ", address["formatted_address"])
                print("This is a parking")
                num_parking += 1
            if 'intersection' in address["types"]:
                print(j, "  ", address["formatted_address"])
                print("This is an intersection")
                num_intersections += 1
            j += 1
    return addresses, num_intersections

def get_intersection_coordinates(text):
    places_result = gmaps.find_place(input=text, input_type='textquery', fields=['geometry'])

    print('places_result   ', places_result["candidates"][0]["geometry"]["location"])

    return places_result

# get_intersection_coordinates('columbia and albert waterloo')

def get_speed_limit(data):
    old_locations=[]
    prev_location = {}

    num_intersections_glbl = 0

    snapped_loc_dict = {}

    for key, cur_location in data.items():
        # print(key, '->', cur_location)
        old_location = cur_location
        old_location['key'] = key
        old_locations.append(old_location)

        if len(old_locations) == 10:
            # print('snapping ', cur)
            snapped_locs_result = gmaps.snap_to_roads(old_locations, interpolate=True)
            print('number of snapped locations found  ', len(snapped_locs_result))

            snapped_locs = []

            for snapped_loc_result in snapped_locs_result:
                snapped_locs.append(snapped_loc_result["location"])

            #get the speed limit
            # speed_limits = gmaps.snapped_speed_limits(snapped_locs)
            speed_limits = []
            print('finding speed limits of ', len(snapped_locs))

            mini_locs = []
            for snapped_loc in snapped_locs:
                mini_locs.append(snapped_loc)
                if len(mini_locs) == 2:
                    print(mini_locs[0], mini_locs[1])
                    speed_url = "https://www.wikispeedia.org/a/marks_bb5.php?name=replitest100&nelat="+str(mini_locs[0]["latitude"])+"&swlat="+str(mini_locs[1]["latitude"])+"&nelng="+str(mini_locs[0]["longitude"])+"&swlng="+str(mini_locs[1]["longitude"])+"&since=2014-07-22"
                    print('speed_url  ', speed_url)
                    contents = urllib.request.urlopen(speed_url).read()

                    root = ET.fromstring(contents)

                    for child in root:
                        print(child.attrib)
                        print(float(child.get('mph'))*1.609344)

                    speed_limit = float(root[-1].get('mph'))*1.609344
                    decimals = 0
                    multiplier = 10 ** decimals
                    speed_limit = math.ceil(speed_limit * multiplier) / multiplier
                    speed_limits.append(speed_limit)
                    speed_limits.append(speed_limit)

                    mini_locs = []

            result_num = 0
            for speed_limit in speed_limits:
                data[result_num]["speed_limit"] = speed_limit
                print(result_num, "  ", data[result_num])
                result_num += 1

            old_locations = []
            break

with open('/Users/kberry/Downloads/20200306-175204.json') as f:
  data = json.load(f)

get_speed_limit(data)


# contents = urllib.request.urlopen("https://www.wikispeedia.org/a/marks_bb5.php?name=replitest100&nelat=35.201&swlat=35.191&nelng=-89.199&swlng=-89.201&since=2014-07-22").read()
#
# root = ET.fromstring(contents)
#
# for child in root:
#     print(child.attrib)
#     print(float(child.get('mph'))*1.609344)

# with open('/Users/kberry/Downloads/20200306-175204_snapped.json', 'w') as outfile:
#     json.dump(snapped_loc_dict, outfile)
