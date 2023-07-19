import json
from random import random
import pandas as pd
import time
from mapcsv import trasform_csv
from mapcsv import document_streets_period

anderlecht = json.load(open('./dataset/Anderlecht_streets.json'))
belgium = json.load(open('./dataset/Belgium_streets.json'))
bruxelles = json.load(open('./dataset/Bruxelles_streets.json'))

street_coordinates = 6
cities = [
    {"name": "anderlecht", "data": anderlecht},
    {"name": "belgium", "data": belgium},
    {"name": "bruxelles", "data": bruxelles}
]

def get_fixed_array_polygon(array, size):
    if len(array) == 0 or len(array) <= size:
        return array

    result = [array[0]]
    size -= 2
    step = len(array) // size

    for i in range(size):
        index = i * step % len(array)
        result.append(array[index])

    result.append(array[0])
    return result

def map_street_to_coordinates(street):
    coords = get_fixed_array_polygon(street["geometry"]["coordinates"][0], street_coordinates)
    return { "coords": coords }

cities_doc = []
for city in cities:
    doc = {
        "name": city["name"],
        "streets": [map_street_to_coordinates(street) for street in city["data"]["features"]]
    }
    cities_doc.append(doc)


file_path = {
    'anderlecht': ['./dataset/And_15min_0101_0103_2019.csv', './dataset/And_15min_0506_1610_2021.csv', './dataset/And_15min_1303_0606_2021.csv'],
    'bruxelles' : ['./dataset/Bxl_15min_0101_0103_2019.csv', './dataset/Bxl_15min_0506_1610_2021.csv', './dataset/Bxl_15min_1303_0606_2021.csv']
}


async def execute(client):
    client["mydb"]["polygons"].insert_many(cities_doc)

    for property_name, periods in file_path.items():
        for i in range(len(periods)):
            grouped_df = trasform_csv(periods[i])
            print("inizio "+ property_name)
            period_streets = document_streets_period(grouped_df)
            client["mydb"][f"{property_name}-period-{i+1}"].insert_many(period_streets)
