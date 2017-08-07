# Develop a program that calculates the distance between two cities
# and allows the user to specify a unit of distance. This program
# may require finding coordinates for the citias like latitude and longitude.
# ---------------- COMPLETED ----------------


import googlemaps
import math


def distance(lat1, lng1, lat2, lng2, radius=6371000):
    a = (math.sin((math.radians(lat2) - math.radians(lat1)) / 2))**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * (math.sin((math.radians(lng2) - math.radians(lng1)) / 2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c


gmaps = googlemaps.Client(key='AIzaSyCdRC5tO_ytMEB4vg1XO-jZzbgLUkK1f9Y')

city1 = gmaps.geocode(input("Type one city: "))[0]
city2 = gmaps.geocode(input("Type another city: "))[0]

print("Calculated distance = {} km".format(distance(city1['geometry']['location']['lat'], city1['geometry']['location']['lng'], city2['geometry']['location']['lat'], city2['geometry']['location']['lng'], ) / 1000))
