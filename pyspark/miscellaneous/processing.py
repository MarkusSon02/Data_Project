from pyspark.sql import SparkSession
from pyspark.sql.functions import isnan, when, count, col

# Step 1: Setup SparkSession
spark = SparkSession.builder \
    .appName("NFL_ETL_Pipeline") \
    .config("spark.jars", "pyspark/postgresql-42.7.4.jar") \
    .getOrCreate()

postgres_url = "jdbc:postgresql://localhost:5432/spotify"
postgres_properties = {
    "user": "son",
    "password": "son",
    "driver": "org.postgresql.Driver"
}


# Step 2: Extract
data = spark.read.csv("data/spotify_data/data.csv", header=True, inferSchema=True)
genre_data = spark.read.csv('data/spotify_data/data_by_genres.csv', header=True, inferSchema=True)
year_data = spark.read.csv('data/spotify_data/data_by_year.csv', header=True, inferSchema=True)

print(data.printSchema())
print(genre_data.printSchema())
print(year_data.printSchema())

# # Step 3: Transform
# # Clean Data
data.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in data.columns]).show()
genre_data.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in genre_data.columns]).show()
year_data.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in year_data.columns]).show()


data.write.jdbc(
    url=postgres_url,
    table="data",
    mode="overwrite",
    properties=postgres_properties
)

genre_data.write.jdbc(
    url=postgres_url,
    table="genre_data",
    mode="overwrite",
    properties=postgres_properties
)

year_data.write.jdbc(
    url=postgres_url,
    table="year_data",
    mode="overwrite",
    properties=postgres_properties
)

# Stop the SparkSession
spark.stop()
