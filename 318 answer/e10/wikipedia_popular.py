import sys
from pyspark.sql import SparkSession, functions, types
import pandas as pd

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+


schema = types.StructType([
    types.StructField('language', types.StringType(), False),
    types.StructField('page', types.StringType(), False),
    types.StructField('views', types.IntegerType(), False),
    types.StructField('bytes', types.IntegerType(), False),
])


def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]

    def spilt(filenmae):
        file = filenmae.rsplit('/', 1)[1]
        date = file.split("-", 1)[1]
        name = date[:-7]
        return name

    path_to_hour = functions.udf(spilt, returnType=types.StringType())
    data = spark.read.csv(in_directory, sep = " ", schema=schema).withColumn('filename', path_to_hour(functions.input_file_name()))

    filter_data = data.filter((data['language'] == "en") & (data["page"] != "Main_Page") & (~data["page"].startswith("Special:"))).drop_duplicates()

    grouped = filter_data.groupby("filename").max("views")

    joined_data = filter_data.join(grouped, on=((filter_data['views'] == grouped['max(views)'])) & (filter_data['filename'] == grouped['filename'])).drop(filter_data['filename'])
    joined_data = joined_data.sort(joined_data['filename'])

    max_view = joined_data.select(joined_data['filename'], joined_data['page'], joined_data['views'])
    max_view.show()

    max_view.write.csv(out_directory + '-max_view', mode='overwrite')

if __name__=='__main__':
    main()