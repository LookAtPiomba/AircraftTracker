from pyopensky import OpenskyImpalaWrapper
import pandas as pd

data = pd.read_csv('data/it-airports.csv', header=0, sep=',', skiprows=[1])

df = data[~data['type'].isin(['heliport', 'closed', 'seaplane_base', 'small_airport'])]
# Filter out rows where the 'name' column contains 'Air Base' as these are military airports
df = df[~df['name'].str.contains('Air Base')]

df.to_csv('data/it-airports-filtered.csv')

airports_ids = df['ident'].unique()

opensky = OpenskyImpalaWrapper()

#search for airplaines that did one of the routes in the last year
list_of_dataframes = []

for id_1 in airports_ids:
    for id_2 in airports_ids:
        if id_1 != id_2:
            list_of_dataframes.append(opensky.rawquery(f"SELECT * FROM flights_data4 WHERE (estdepartureairport='{id_1}' AND estarrivalairport='{id_2}') AND (day BETWEEN 1641043200 AND 1672540799);"))

routes = pd.concat(list_of_dataframes)
routes.to_csv('routes.csv')

