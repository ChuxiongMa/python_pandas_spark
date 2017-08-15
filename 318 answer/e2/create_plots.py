import sys
import pandas as pd
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]

data1 = pd.read_table(filename1, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])
data2 = pd.read_table(filename2, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

sorted1 = data1.sort_values(["views"], ascending=False)
sorted2 = data2.sort_values(["views"], ascending=False)
sorted1['rank'] = range(1, len(sorted1) + 1)

s1 = pd.Series(sorted1["views"], name='views1')
s2 = pd.Series(sorted2["views"], name='views2')
df = pd.concat([s1, s2], axis=1)

plt.figure(figsize=(10, 5))
f1 = plt.subplot(1, 2, 1)
plt.plot(sorted1['rank'].values, sorted1['views'].values, 'r-', linewidth=1)
f1.set_title('Popularity Distribution')
f1.set_xlabel('Rank')
f1.set_ylabel('Views')
#
f2 = plt.subplot(1, 2, 2)
plt.plot(df['views1'].values, df['views2'].values, 'b.', alpha=0.5)
f2.set_title('Daily Correlation ')
f2.set_xlabel('Day 1 views')
f2.set_ylabel('Day 2 views')
plt.xscale('log')
plt.yscale('log')
plt.savefig('wikipedia.png')
