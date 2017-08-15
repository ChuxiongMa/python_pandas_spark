from pykalman import KalmanFilter
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import sys

filename = sys.argv[1]
lowess = sm.nonparametric.lowess

cpu_data = pd.read_csv(filename, parse_dates=['timestamp'])

kalman_data = cpu_data[['temperature', 'cpu_percent']]
initial_state = kalman_data.iloc[0]

observation_stddev = 1
transition_stddev = 0.5
observation_covariance = [[observation_stddev ** 2, 0], [0, 2 ** 2]]
transition_covariance = [[transition_stddev ** 2, 0], [0, 80 ** 2]]
transition_matrix = [[1, 0.125], [0, 1]]

kf = KalmanFilter(
    initial_state_mean=initial_state,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition_matrix)

plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)

loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp'],frac=0.06)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')

kalman_smoothed, _ = kf.smooth(kalman_data)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
# plt.show()
plt.savefig('cpu.svg')
