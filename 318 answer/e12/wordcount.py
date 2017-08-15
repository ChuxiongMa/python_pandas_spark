​​​​​import sys
from pyspark.sql import SparkSession, functions, types, Row
import re, math
import numpy as np
import string, re


spark = SparkSession.builder.appName('word_count').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+



def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    df = spark.read.text(in_directory)
    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)
    splited = df.select(functions.explode(functions.split(df.value, wordbreak)).alias('word'))
    splited = splited.filter(splited['word'] != '')
    lower = splited.select(functions.lower(splited['word']).alias('word'))
    
    groupped = lower.groupby('word')
    count = groupped.agg(functions.count(lower['word']))
    count = count.sort(count['count(word)'], ascending=False)
    count.show()
    count.write.csv(out_directory, mode='overwrite')



if __name__=='__main__':
    main()
