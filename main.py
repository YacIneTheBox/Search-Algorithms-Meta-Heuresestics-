import csv
import random
import math
import copy

class City:
    def __init__(self,name,lat,lon,x,y):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.x = x
        self.y = y

cities = []

with open('algeria_20_cities_xy.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        
        name,lat,lon,x,y = row
        city = City(name,float(lat),float(lon),float(x),float(y))
        cities.append(city)
    

def distance(city1, city2):
    x1 = city1.x
    y1 = city1.y
    x2= city2.x
    y2 = city2.y
    
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)    

def total_distance(route):
    dist = 0
    for i in range(len(route) - 1):
        dist += distance(route[i], route[i + 1])
    # Retour à la ville de départ
    dist += distance(route[-1], route[0])
    return dist


    
def Random_search(cities,iteration):
    nbrCities = len(cities)
    sCity = "Algiers"
    totalDistance = 0
    shortestDistance = float('inf')
    clonCities = copy.deepcopy(cities)
         
    for l in range(iteration):
        random.shuffle(clonCities)
        index = next(i for i, city in enumerate(clonCities) if city.name == sCity)
        clonCities[0],clonCities[index] = clonCities[index],clonCities[0]    
        totalDistance = total_distance(clonCities)
        
        if totalDistance < shortestDistance:
            shortestDistance = totalDistance
            
    return shortestDistance

iteration = 1000
shortestDist = Random_search(cities,iteration)
print ('The shortest path is : ',shortestDist)


