import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col,to_date
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format,dayofweek,monotonically_increasing_id
from pyspark.sql.types import TimestampType, DateType,IntegerType

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['KEYS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['KEYS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    create a spark session with return of spark
    return: spark session aka spark
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Process song data to
    Read data from S3 by input_data and write them back to S3 with output data
    Here with the song_data
    Args:
        - spark: spark session
        - input_data_song: input data song s3 linke
        - output_data: my own s3 bucket (set in public)
    """
    # get filepath to song data file
    song_data = "{}/song_data/A/A/A/*.json".format(input_data)
    
    # read song data file
    df = spark.read.json(song_data).dropDuplicates().cache()

    # extract columns to create songs table
    songs_table = df.select(col("song_id"),col("title"),col("artist_id"),col("year"),col("duration")).distinct()

    # write songs table to parquet files partitioned by year and artist
    songs_table.write.parquet(output_data + "songs_table/", mode="overwrite",partitionBy=["year","artist_id"])

    # extract columns to create artists table
    artists_table =df.select("artist_id","artist_name","artist_location","artist_latitude","artist_longitude").dropDuplicates()

    # write artists table to parquet files
#     artists_table.write.parquet("s3://aws-emr-resources-799099438146-us-east-1/Sparkify/artists_table.parquet".format(output_data))
    artists_table.write.parquet(output_data + "artists_table/",mode="overwrite")
    df.createOrReplaceTempView("song_table")

def process_log_data(spark, input_data, output_data):
    """
    Read data from S3 by input_data and write them back to S3 with output data
    Here with the log_data
    Args:
        - spark: spark session
        - input_data_log: input data logs s3 link
        - output_data: My own s3 bucket (set in public)
    """
    # get filepath to log data file
    log_data = "s3a://udacity-dend/log_data/*/*/*events.json".format(input_data)

    # read log data file
    df = spark.read.json(log_data).dropDuplicates().cache()

    # filter by actions for song plays
    df = df.filter(df.page == "NextSong").cache()

    # extract columns for users table
    users_table =df.select(col("firstName"), col("lastName"), col("gender"), col("level"), col("userId")).distinct()

    # write users table to parquet files
    users_table.write.parquet(output_data+"users_table/",mode="overwrite")

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x:datetime.fromtimestamp(x/1000),TimestampType())
    df = df.withColumn("timestamp",get_timestamp(col("ts")))

    # create datetime column from original timestamp column
    get_datetime = udf(lambda x :to_date(x),TimestampType())
    df =df.withColumn("start_time",get_datetime(col("ts")))

    # extract columns to create time table
    df = df.withColumn("hour", hour("timestamp"))
    df = df.withColumn("day", dayofmonth("timestamp"))
    df = df.withColumn("month", month("timestamp"))
    df = df.withColumn("year" , year("timestamp"))
    df = df.withColumn("week", weekofyear("timestamp"))
    df = df.withColumn("weekday",dayofweek("timestamp"))
    time_table = df.select(col("start_time"),col("hour"), col("day"), col("month"),col("year"),col("week"),col("weekday")).distinct()

    # write time table to parquet files partitioned by year and month
    time_table.write.parquet(output_data+"time/",mode="overwrite",partitionBy=["year","month"])

    # read in song data to use for songplays table
    song_df = spark.sql("select distinct song_id, artist_id, artist_name from songs_table")

    # extract columns from joined song and log datasets to create songplays table
    songplays_table =df.join(song_df , song_df.artist_name == df.artist, "inner").distinct().\
                        df.select(col("start_time"), col("userId"), col("level"), col("sessionId"), \
                col("location"), col("userAgent"), col("song_id"), col("artist_id"),col("year"), col("month"))\
                .withColumn("songplay_id", monotonically_increasing_id())

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.parquet(output_data+"songplays_table/",mode="overwrite",partitionBy=["year","month"])


def main():
    """
    Operating function
    """
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://awsbucket41/Sparkify/"

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
