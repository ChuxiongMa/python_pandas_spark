import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from pykalman import KalmanFilter
import sys


def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)

    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)

    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)

    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


def distance(position):
    position_shift = position.shift(periods=-1, freq=None, axis=0)
    p = 0.017453292519943295
	
	#reference: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
    a = 0.5 - np.cos((position_shift['lat'] - position['lat']) * p) / 2 + np.cos(position['lat'] * p) * np.cos(
        position_shift['lat'] * p) * (1 - np.cos((position_shift['lon'] - position['lon']) * p)) / 2  
    return np.sum(12742 * 1000 * np.arcsin(np.sqrt(a)))


def get_data(path):
    data = ET.parse(path)
    root = data.getroot()
    lat = []
    lon = []

    for trk in root.iter('{http://www.topografix.com/GPX/1/0}trkpt'):
        lat.append(trk.attrib['lat'])
        lon.append(trk.attrib['lon'])

    position = pd.DataFrame(lat, columns=['lat'])
    position['lon'] = lon

    position['lat'] = position['lat'].astype('float64')
    position['lon'] = position['lon'].astype('float64')

    return position


def smooth(position):
    initial_state = position.iloc[0]
    observation_stddev = 0.000001
    transition_stddev = 0.00000035
    observation_covariance = [[observation_stddev ** 2, 0], [0, 0.000005 ** 2]]
    transition_covariance = [[transition_stddev ** 2, 0], [0, 0.00000105 ** 2]]
    transition_matrix = [[1, 0], [0, 1]]

    kf = KalmanFilter(
        initial_state_mean=initial_state,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition_matrix)

    kalman_smoothed, _ = kf.smooth(position)

    some_data = pd.DataFrame(kalman_smoothed[:, 0], columns=['lat'])
    some_data['lon'] = kalman_smoothed[:, 1]
    return some_data


def main():
    points = get_data(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points),))

    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()
