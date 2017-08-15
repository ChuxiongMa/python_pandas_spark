import numpy as np
import pandas as pd
import glob
import os
from sklearn.decomposition import PCA
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier,AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
import sys
from os import listdir
from os.path import isfile, join
from PIL import Image

# retreive the date time sequence in the file name
def fileToTime(x):
    return x[7:19]

# function apply to the weather conditon column
# to simplify certain weather condition string
def cleanUpWeatherCond(x):
    if (x == "Clear") or ("Clear" in x):
        return "Clear"
    elif (x == "Cloudy") or ("Cloudy" in x):
        return "Cloudy"
    elif ("Rain" in x) and ("Snow" in x) and ("Fog" in x):
        return "Rain,Snow,Fog"
    elif ("Rain" in x) and ("Snow" in x):
        return "Rain,Snow"
    elif ("Rain" in x) and ("Fog" in x):
        return "Rain,Fog"
    elif ("Drizzle" in x) and ("Fog" in x):
        return "Rain,Fog"
    elif ("Snow" in x) and ("Fog" in x):
        return "Snow,Fog"
    elif (x == "Snow") or ("Snow" in x):
        return "Snow"
    elif (x == "Rain") or ("Rain" in x):
        return "Rain"
    elif (x == "Drizzle") or ("Drizzle" in x):
        return "Rain"
    elif (x == "Thunderstorms") or ("Thunderstorms" in x):
        return "Rain"
    elif (x == "Fog") or ("Fog" in x):
        return "Fog"
    else:
        return x


def WeatherToArray(x):
    return x.split(",")


def main():
    # algorithm for reading csv file in a folder is provided at:
    # https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe

    # run with command: python3 weather_predict.py ./yvr-weather ./katkam-scaled output

    path = sys.argv[1]
    image_path = sys.argv[2]
    output = sys.argv[3]
    allFiles = glob.glob(os.path.join(path, "*.csv"))

    weather_data = pd.DataFrame()
    list_ = []

    for file_ in allFiles:
        df = pd.read_csv(file_, skiprows=16)
        list_.append(df)

    weather_data = pd.concat(list_, ignore_index=True)
    date_weather = weather_data[['Date/Time', 'Weather']]
    date_weather['Date/Time'] = pd.to_datetime(date_weather['Date/Time'])

    # reading the image files name
    # logic provided at: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    image_names = [f for f in listdir(image_path) if isfile(join(image_path, f))]

    # convert the data time sequence in the file name to date time
    image_df = pd.DataFrame(image_names, dtype='str', columns=['fileName'])
    image_df['Date/Time'] = pd.to_datetime(image_df['fileName'].apply(fileToTime))
    image_df['fileName'] = image_path + "/" + image_df['fileName']

    # join weather condition data with corresponding image
    joined_df = image_df.join(date_weather.set_index('Date/Time'), on='Date/Time')
    joined_df = joined_df[joined_df['Weather'].notnull()].reset_index(drop=True)
    joined_df['month']= joined_df['Date/Time'].dt.month
    joined_df['hour'] = joined_df['Date/Time'].dt.hour
    

    #Image cleaning
    # each df will store the file name of images that are completely black at night
    # each df represent a different month
    df1 = joined_df[(joined_df['month'] == 10) & ((joined_df['hour'] == 6) | (joined_df['hour'] == 7)
                                                | (joined_df['hour'] == 17) | (joined_df['hour'] == 18)
                                                | (joined_df['hour'] == 19)| (joined_df['hour'] == 20))]

    df2 = joined_df[(joined_df['month'] == 11) & ((joined_df['hour'] == 6) | (joined_df['hour'] == 7)
                                                | (joined_df['hour'] == 17) | (joined_df['hour'] == 18))]

    df3 = joined_df[(joined_df['month'] == 12) & ((joined_df['hour'] == 6) | (joined_df['hour'] == 7)
                                                | (joined_df['hour'] == 17) | (joined_df['hour'] == 18)
                                                | (joined_df['hour'] == 19) | (joined_df['hour'] == 20))]


    df4 = joined_df[(joined_df['month'] == 1) & ((joined_df['hour'] == 6) | (joined_df['hour'] == 7)
                                                | (joined_df['hour'] == 17) | (joined_df['hour'] == 18)
                                                | (joined_df['hour'] == 19) | (joined_df['hour'] == 20))]


    df5 = joined_df[(joined_df['month'] == 2) & ((joined_df['hour'] == 6) | (joined_df['hour'] == 7)
                                                | (joined_df['hour'] == 17) | (joined_df['hour'] == 18)
                                                | (joined_df['hour'] == 19) | (joined_df['hour'] == 20))]

    df6 = joined_df[(joined_df['month'] == 6) & ((joined_df['hour'] == 20 | (joined_df['hour'] == 21)))]

    df7 = joined_df[(joined_df['month'] == 7) & ( (joined_df['hour'] == 20| (joined_df['hour'] == 21)))]

    df8 = joined_df[(joined_df['month'] == 8) & ((joined_df['hour'] == 20))]

    df9 = joined_df[(joined_df['month'] == 9) & ((joined_df['hour'] == 6) | (joined_df['hour'] == 20))]

    df10 =joined_df[(joined_df['month'] == 3) & ((joined_df['hour'] == 6) | (joined_df['hour'] == 7)
                                               | (joined_df['hour'] == 17) | (joined_df['hour'] == 18)
                                               | (joined_df['hour'] == 19))]

    df11 = joined_df[(joined_df['month'] == 4) & ((joined_df['hour'] == 6))]

    df12 = joined_df[(joined_df['month'] == 5) & ((joined_df['hour'] == 19) | (joined_df['hour'] == 20))]

    # concat reference: https://stackoverflow.com/questions/44781950/pandas-merge-two-data-frames-and-keep-non-intersecting-data-from-a-single-data
    joined_df = pd.concat([joined_df, df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]).drop_duplicates(keep=False)

    joined_df['cleaned_Weather'] = joined_df['Weather'].apply(cleanUpWeatherCond)
    
    weather_arr = joined_df['cleaned_Weather'].apply(WeatherToArray).as_matrix()

    mlb = MultiLabelBinarizer()
    mlb_arr = mlb.fit_transform(weather_arr)  # the y array which will be used in the model

    # read photo using pillow

    image_arr = joined_df['fileName'].as_matrix()
    image_list = []

    for file in image_arr:
        im = Image.open(file)
        image_list.append(np.asarray(im))
        im.close()


    image_list = np.asarray(image_list)
    image_list = image_list.reshape(image_list.shape[0], -1)
    pca = PCA(500)
    pca.fit(image_list)
    X_pca = pca.transform(image_list)
    X_train, X_test, y_train, y_test = train_test_split(X_pca, mlb_arr)

    # the usage of bagging classifier is provided at:
    # https://stackoverflow.com/questions/18165213/how-much-time-does-take-train-svm-classifier
    n_estimators = 150
    seed = 12

    #model  OneVsRestClassifier(BaggingClassifier(SVC(kernel='linear', probability=True, class_weight='balanced'),max_samples=1.0 / n_estimators, n_estimators=n_estimators))
    #model = OneVsRestClassifier(AdaBoostClassifier(n_estimators=n_estimators,random_state=seed))
    model = OneVsRestClassifier(GradientBoostingClassifier(n_estimators=n_estimators, random_state=seed))
    model.fit(X_train, y_train)
    y_predicted = model.predict(X_test)
    print(accuracy_score(y_test, y_predicted))

    # convert the binarized array back to class label
    # and output them as csv file
    output_y_predicted = np.asarray(mlb.inverse_transform(y_predicted))
    output_y_test = np.asarray(mlb.inverse_transform(y_test))
    compare = pd.DataFrame({'predicted':output_y_predicted, 'actual':output_y_test})
    compare.to_csv(output, index = False)


if __name__ == '__main__':
    main()
