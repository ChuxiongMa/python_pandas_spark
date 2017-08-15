import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

schema = types.StructType([ # commented-out fields won't be read
    #types.StructField('archived', types.BooleanType(), False),
    types.StructField('author', types.StringType(), False),
    #types.StructField('author_flair_css_class', types.StringType(), False),
    #types.StructField('author_flair_text', types.StringType(), False),
    #types.StructField('body', types.StringType(), False),
    #types.StructField('controversiality', types.LongType(), False),
    #types.StructField('created_utc', types.StringType(), False),
    #types.StructField('distinguished', types.StringType(), False),
    #types.StructField('downs', types.LongType(), False),
    #types.StructField('edited', types.StringType(), False),
    #types.StructField('gilded', types.LongType(), False),
    #types.StructField('id', types.StringType(), False),
    #types.StructField('link_id', types.StringType(), False),
    #types.StructField('name', types.StringType(), False),
    #types.StructField('parent_id', types.StringType(), True),
    #types.StructField('retrieved_on', types.LongType(), False),
    types.StructField('score', types.LongType(), False),
    #types.StructField('score_hidden', types.BooleanType(), False),
    types.StructField('subreddit', types.StringType(), False),
    #types.StructField('subreddit_id', types.StringType(), False),
    #types.StructField('ups', types.LongType(), False),
])


def main():
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]

    comments = spark.read.json(in_directory, schema=schema)
    comments_cache = comments.cache()

    # TODO
    average_score = comments_cache.groupBy("subreddit").mean()
    average_score = average_score.filter(average_score["avg(score)"] > 0)
    average_score = functions.broadcast(average_score)

    join_average_score = average_score.join(comments_cache, on=(average_score['subreddit'] == comments_cache['subreddit'])).drop(average_score['subreddit'])
    join_average_score_cache = join_average_score.cache()

    relative_score = join_average_score_cache.select(join_average_score_cache['subreddit'], join_average_score_cache['author'], (join_average_score_cache['score']/join_average_score_cache['avg(score)']).alias("relative_score"))
    relative_score_cache = relative_score.cache()

    max_relative = relative_score_cache.groupby('subreddit').max('relative_score')
    max_relative = functions.broadcast(max_relative)


    best_comment = max_relative.join(relative_score_cache, on=(max_relative['max(relative_score)'] == relative_score_cache['relative_score'])).drop(max_relative['max(relative_score)']).drop(max_relative['subreddit'])
    best_comment_cache = best_comment.cache()

    best_author = best_comment_cache.sort(best_comment_cache['subreddit'])
    best_author.show()

    best_author.write.json(out_directory, mode='overwrite')


if __name__=='__main__':
    main()
