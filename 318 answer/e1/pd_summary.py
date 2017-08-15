import pandas as pd

totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

city_total = totals.sum(axis=1)

print "City with lowest total preciptiation:"
print city_total.argmin()

print "Average precipitation in each month:"
month_total = totals.sum(axis=0)
count_total = counts.sum(axis=0)
print month_total/count_total

print "Average precipitation in each city:"
count_total = counts.sum(axis=1)
print city_total/count_total

