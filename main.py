import csv

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
        print (row)