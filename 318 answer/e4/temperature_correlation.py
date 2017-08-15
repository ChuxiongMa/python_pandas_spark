import pandas as pd
import numpy as np
import gzip
import matplotlib.pyplot as plt
import sys

filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = sys.argv[3]

station_fh = gzip.open(filename1, 'rt', encoding='utf-8')
stations = pd.read_json(station_fh, lines=True)
stations["avg_tmax"] = stations["avg_tmax"]/10
# print (stations)

city_data =  pd.read_csv(filename2)
city_data=city_data.dropna()
city_data["area"] = city_data["area"]/1000000
city_data = city_data[city_data.area <= 10000].reset_index()
del city_data["index"]
city_data["density"] = city_data["population"]/city_data["area"]
# print(city_data)


def distance(city, stations):
    p = 0.017453292519943295

    # logic copied from: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
    a = 0.5 - np.cos((stations['latitude'] - city['latitude']) * p) / 2 + np.cos(city['latitude'] * p) * np.cos(
        stations['latitude'] * p) * (1 - np.cos((stations['longitude'] - city['longitude']) * p)) / 2
    return 12742 * np.arcsin(np.sqrt(a))


def best_tmax(city, stations):
    index = np.argmin(distance(city, stations))
    return stations["avg_tmax"][index]


maxt = city_data.apply(best_tmax, stations=stations, axis=1)

f1 = plt.subplot()
f1.set_title('Temperature vs Population Density')
f1.set_xlabel('Avg Max Temperature (\u00b0C)')
f1.set_ylabel('Population Density (people/km\u00b2)')


plt.plot(maxt, city_data['density'], 'b.', alpha=0.5)
plt.savefig(filename3)