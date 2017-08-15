import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import sys


labelled = pd.read_csv(sys.argv[1])
unlabelled = pd.read_csv(sys.argv[2])

weather_data = labelled.as_matrix(columns=labelled.columns[2:62])
cities = labelled.as_matrix(columns=labelled.columns[0:1])

X_train, X_test, y_train, y_test = train_test_split(weather_data, cities)

weather_data_test = unlabelled.as_matrix(columns=unlabelled.columns[2:62])

y = y_train.ravel()
y_train = np.array(y).astype(str)

model = make_pipeline(
    StandardScaler(),
    SVC()
)
model.fit(X_train, y_train)
print(X_train.shape)
print(y_train.shape)

cities_predicted = model.predict(weather_data_test)
# print (cities_predicted)

lab_y_predicted = model.predict(X_test)
print(accuracy_score(y_test, lab_y_predicted))

pd.Series(cities_predicted).to_csv(sys.argv[3], index=False)
