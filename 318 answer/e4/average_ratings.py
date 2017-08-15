import pandas as pd
import difflib
import sys

filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = sys.argv[3]

movies = pd.read_table(filename1, names=["movie"])
rating = pd.read_csv(filename2)


def match(data):
    return "".join(difflib.get_close_matches(data, movies["movie"]))

matched = rating.title.apply(match)
rating["title"] = matched

grouped_data = rating.groupby(['title'])
sum_data = grouped_data.aggregate('sum')
count_data = grouped_data.aggregate('count')
result = sum_data/count_data

result = result.ix[1:]
movies["rating"] = result["rating"]
data = result.round(2)
print (data)

data.to_csv(filename3, sep=',')
