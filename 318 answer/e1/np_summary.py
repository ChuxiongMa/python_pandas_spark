import numpy as np

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

city_sum = np.sum(totals, axis=1)

print "Row with lowest total preciptiation:"
print np.argmin(city_sum)

print "Average precipitation in each month:"
month_sum = np.sum(totals, axis=0)
month_count = np.sum(counts, axis=0)
x=month_sum.astype(np.float)
print x/month_count

print "Average precipitation in each city:"
city_count = np.sum(counts, axis=1)
y=city_sum.astype(np.float)
print y/city_count

print "Quarterly precipitation totals:"
reshape = np.reshape(totals, (36,3))
reshape_sum = np.sum(reshape, axis=1)
print np.reshape(reshape_sum, (12,3))
