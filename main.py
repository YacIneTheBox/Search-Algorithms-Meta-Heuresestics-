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
        city = City(name,lat,lon,x,y)
        cities.append(city)
        
for c in cities:
    print(f"{c.name}: ({c.x},{c.y})")
    
    
def Random_search(cities,iteration):
    nbrCities = cities.size()
    sCity = "Algiers"
    totalDistance = 0
    shortestDistance = float('inf')
    clonCities = copy.deepcopy(cities)
         
    for l in range(iteration):
        for j in range(nbrCities):
            random.shuffle(clonCities)
            index = next(i for i, city in enumerate(clonCities) if city.name == sCity)
            totalDistance += math.dist([clonCities[index].x,clonCities[index].y],[clonCities[j].x,clonCities[j].y])
        
        if totalDistance < shortestDistance:
            shortestDistance = totalDistance
            
        totalDistance = 0
    return shortestDistance

iteration = 10
shortestDist = Random_search(cities,iteration)