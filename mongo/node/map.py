import pandas as pd
import time

def trasform_csv(file):
    df = pd.read_csv(file, header=None)
    df = df.rename(columns={0: 'index_row', 1: 'index_street', 2: 'traffic', 3: 'velocity'})

    int_columns = df.columns[1:]
    df[int_columns] = df[int_columns].astype(int)

    df.sort_values(by='index_street', inplace=True)
    grouped = df.groupby('index_street')

    return df

file_path = ['./dataset/And_15min_0101_0103_2019.csv', './dataset/And_15min_0506_1610_2021.csv', './dataset/And_15min_1303_0606_2021.csv']

start_time = time.time()

anderlecht_data = []
for i in range(len(file_path)):
    anderlecht_data.append(trasform_csv(file_path[i]))

elapsed_time = time.time() - start_time
print("Tempo di esecuzione:", elapsed_time, "secondi")