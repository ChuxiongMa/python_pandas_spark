import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


data = pd.read_csv("data.csv")
mean_time = data.groupby("name").agg("mean")
print (mean_time)

qs1 = data[data.name == "qs1"].reset_index()
qs2 = data[data.name == "qs2"].reset_index()
qs3 = data[data.name == "qs3"].reset_index()
qs4 = data[data.name == "qs4"].reset_index()
qs5 = data[data.name == "qs5"].reset_index()
merge1 = data[data.name == "merge1"].reset_index()
partition_sort = data[data.name == "partition_sort"].reset_index()

anova = stats.f_oneway(qs1["time"], qs2["time"], qs3["time"], qs4["time"], qs5["time"], merge1["time"], partition_sort["time"])
print(anova)
print(anova.pvalue)

# print (data)
x_data = pd.DataFrame({'qs1': qs1['time'], 'qs2': qs2['time'], 'qs3': qs3['time'], 'qs4': qs4['time'], 'qs5': qs5['time'], 'merge1': merge1['time'], 'partition_sort': partition_sort['time']})
#
x_melt = pd.melt(x_data)
posthoc = pairwise_tukeyhsd(
    x_melt['value'], x_melt['variable'],
    alpha=0.05)

print (posthoc)

fig = posthoc.plot_simultaneous()
fig.set_size_inches((15, 12))
fig.savefig("output.png")