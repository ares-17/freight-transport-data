import pandas as pd

def trasform_csv(file):
    df = pd.read_csv(file, header=None)
    df = df.rename(columns={0: 'datetime', 1: 'index_street', 2: 'traffic', 3: 'velocity'})

    int_columns = df.columns[1:]
    df[int_columns] = df[int_columns].astype(int)

    df.sort_values(by='index_street', inplace=True)
    grouped = df.groupby('index_street')
    #grouped = grouped.apply(lambda x: x.drop('index_street', axis=1))
    
    return grouped

def document_streets_period(grouped_df):
    period_streets = []
    i = 0
    for group_name, group_data in grouped_df:
        if pd.isnull(group_name):
            group_name = i
        period_streets.append({
            'id': group_name,
            'events': group_data.to_dict('records'),
            'traffic_mean': group_data['traffic'].mean(),
            'velocity_mean': group_data['velocity'].mean()})
        i = i + 1
    return period_streets
