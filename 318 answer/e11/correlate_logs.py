import sys
from pyspark.sql import SparkSession, functions, types, Row
import re, math
import numpy as np

spark = SparkSession.builder.appName('correlate logs').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

line_re = re.compile("^(\\S+) - - \\[\\S+ [+-]\\d+\\] \"[A-Z]+ \\S+ HTTP/\\d\\.\\d\" \\d+ (\\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        host, tail = line.split('- -')
        bytes=tail.rsplit(' ', 1)[1]
        return Row(hostname=host, bytes=bytes)
    else:
        return None

def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    rows = log_lines.map(line_to_row).filter(not_none)
    return rows
    # TODO: return an RDD of Row() objects


def main():
    in_directory = sys.argv[1]
    logs = spark.createDataFrame(create_row_rdd(in_directory))

    groups = logs.groupby('hostname')
    result = groups.agg(functions.count(logs['hostname']).alias('count'), functions.sum(logs['bytes']).alias('total_bytes'))

    data = result.select(result['count'].alias('x'), result['total_bytes'].alias('y'), (result['count']**2).alias('x^2'),
                         (result['total_bytes'] ** 2).alias('y^2'), (result['total_bytes']*result['count']).alias('xy'))

    sum = data.select(functions.sum(data['x']),functions.sum(data['y']), functions.sum(data['x^2']), functions.sum(data['y^2']),
                      functions.sum(data['xy']))

    data_point_sum = result.count()
    sum = sum.first()
    # TODO: calculate r.

    r = sum['sum(xy)']
    r = ((data_point_sum*sum['sum(xy)'] - (sum['sum(x)']*sum['sum(y)']))/((math.sqrt(data_point_sum*sum['sum(x^2)']-(sum['sum(x)']**2)))*(math.sqrt(data_point_sum*sum['sum(y^2)']-(sum['sum(y)']**2)))))
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    main()