from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Step 1: Setup SparkSession
spark = SparkSession.builder \
    .appName("NFL_ETL_Pipeline") \
    .getOrCreate()



# Step 2: Extract
file_path = "/home/markus/.cache/kagglehub/datasets/maxhorowitz/nflplaybyplay2009to2016/versions/6/NFL Play by Play 2009-2016 (v3).csv"
raw_data = spark.read.csv(file_path, header=True, inferSchema=True)

# Step 3: Transform
# Clean Data
clean_data = raw_data.dropna(subset=["team", "points", "games"])

# Add Calculated Columns
transformed_data = clean_data.withColumn("points_per_game", col("points") / col("games"))

# Filter for Recent Seasons
recent_seasons_data = transformed_data.filter(col("season") >= 2020)

# Aggregate Data
aggregated_data = recent_seasons_data.groupBy("team").agg({"points_per_game": "avg"})

# Step 4: Load
aggregated_data.write.csv("output_directory", header=True, mode="overwrite")

# Stop the SparkSession
spark.stop()
