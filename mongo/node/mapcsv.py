import pandas as pd

def trasform_csv(file):
    df = pd.read_csv(file, header=None)
    df = df.rename(columns={0: 'datetime', 1: 'index_street', 2: 'traffic', 3: 'velocity'})

    # seleziono tutte le colonne a partire dalla seconda per associare il tipo int
    int_columns = df.columns[1:]
    df[int_columns] = df[int_columns].astype(int)

    df = df[df['datetime'] != ""]  # Scarta le righe con valore vuoto nella colonna 'datetime'

    df.sort_values(by='index_street', inplace=True)
    grouped = df.groupby('index_street')
    
    return grouped

def grouping_by_date(group_name, group_data):
    try:
        group_data_format = group_data.copy()
        group_data_format['datetime'] = pd.to_datetime(group_data_format['datetime'], format="%Y-%m-%d %H:%M:%S")
        group_data_format['day'] = group_data_format['datetime'].dt.date
        group_by_date = group_data_format.groupby('day')

        events = []
        for group_name_d, group_data_d in group_by_date:
            key = group_name_d.strftime("%Y-%m-%d")
            events.append({
                'date' : key,
                'traffic_sum': group_data_d['traffic'].sum().item(),
                'velocity_mean': group_data_d['velocity'].mean(),
            })
        return events
    except Exception as error:
        print(group_name)
        print(error)

def grouping_by_month(group_name, group_data):
    try:
        group_data_format = group_data.copy()
        group_data_format['datetime'] = pd.to_datetime(group_data_format['datetime'], format="%Y-%m-%d %H:%M:%S")
        group_data_format['month'] = group_data_format['datetime'].dt.to_period('M')
        group_by_month = group_data_format.groupby('month')

        events = []
        for group_name_m, group_data_m in group_by_month:
            key = group_name_m.strftime("%Y-%m")
            daily_records = grouping_by_date(group_name_m, group_data_m)
            events.append({
                'date' : key,
                'traffic_sum': group_data_m['traffic'].sum().item(),
                'velocity_mean': group_data_m['velocity'].mean(),
                'events': daily_records
            })

        return events
    except Exception as error:
        print(group_name)
        print(error)


def document_streets_period(grouped_df):
    period_streets = []
    i = 0
    for group_name, group_data in grouped_df:
        if pd.isnull(group_name):
            group_name = i

        document = {
            'id': group_name,
            'traffic_sum': group_data['traffic'].sum().item(),
            'velocity_mean': group_data['velocity'].mean(),
            'events': grouping_by_month(group_name, group_data)
        }
        period_streets.append(document)

        i = i + 1

    return period_streets
