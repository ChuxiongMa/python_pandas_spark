import time
from implementations import all_implementations
import numpy as np
import random
import pandas as pd

name = []
time_length = []


def sort_call():
    random_array = np.array([])

    for num in range(100000):
        random_array = np.append(random_array, [random.randint(-100000, 100000)])

    for sort in all_implementations:
        st = time.time()
        res = sort(random_array)
        en = time.time()
        name.append(sort.__name__)
        time_length.append(en - st)

for num in range(5):
    sort_call()

data = pd.DataFrame({"name": name, "time": time_length})

print (data)
data.to_csv('data.csv', index=False)