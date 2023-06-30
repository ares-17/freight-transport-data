import json
from random import random
import pandas as pd
import time

anderlecht = json.load(open('./dataset/Anderlecht_streets.json'))
belgium = json.load(open('./dataset/Belgium_streets.json'))
bruxelles = json.load(open('./dataset/Bruxelles_streets.json'))

max_val = 10
min_val = 1
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
    step = len(array)

    for i in range(size):
        index = i * step % len(array)
        result.append(array[index])

    result.append(array[0])
    return result

def map_street_to_coordinates(street):
    coords = get_fixed_array_polygon(street["geometry"]["coordinates"][0], street_coordinates)
    return {
        "coords": coords,
        "traffic": random() * (max_val - min_val) + min_val,
        "velocity": 0
    }

documents = []
for city in cities:
    doc = {
        "name": city["name"],
        "streets": [map_street_to_coordinates(street) for street in city["data"]["features"]]
    }
    documents.append(doc)


"""
---- CSV ----
"""

def trasform_csv(file):
    df = pd.read_csv(file, header=None)
    df = df.rename(columns={0: 'index_row', 1: 'index_street', 2: 'traffic', 3: 'velocity'})

    int_columns = df.columns[1:]
    df[int_columns] = df[int_columns].astype(int)

    df.sort_values(by='index_street', inplace=True)
    grouped = df.groupby('index_street')

    return grouped

file_path = ['./dataset/And_15min_0101_0103_2019.csv', './dataset/And_15min_0506_1610_2021.csv', './dataset/And_15min_1303_0606_2021.csv']


async def execute(client):
    client["mydb"]["polygons"].insert_many(documents)

    for i in range(len(file_path)):
        grouped_df = trasform_csv(file_path[i])
        events_period = []
        for group_name, group_data in grouped_df:
            events = []
            for _, row in group_data.iterrows():
                events.append({ "index_street" : row['index_street'], "traffic": row['traffic'], "velocity" : row['velocity']})
            events_streets = { "index": group_data, "events": events}
            events_period.append(events_streets)

        client["mydb"]["anderlecht"][f"period-{i+1}"].insert_many(events_period)
        print(f"executed period {i+1}")

