import pandas as pd
import subprocess

# Load a sample of the dataset
file_path = "/home/markus/.cache/kagglehub/datasets/maxhorowitz/nflplaybyplay2009to2016/versions/6/NFL Play by Play 2009-2016 (v3).csv"
df = pd.read_csv(file_path, nrows=100)  # Load only the first 100 rows to infer schema

# Function to map Pandas types to SQL types for Flink SQL
def infer_sql_type(series):
    if pd.api.types.is_integer_dtype(series):
        return "INT"
    elif pd.api.types.is_float_dtype(series):
        return "DOUBLE"
    elif pd.api.types.is_bool_dtype(series):
        return "BOOLEAN"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "TIMESTAMP"
    else:
        return "STRING"

# Generate schema dynamically
schema = ",\n".join([f"  {col} {infer_sql_type(df[col])}" for col in df.columns])

# Generate Flink SQL DDL
ddl = f"""
CREATE TABLE nfl_data (
{schema}
) WITH (
  'connector' = 'filesystem',
  'path' = '{file_path}',
  'format' = 'csv'
);
"""

# Pass schema to the Java program
subprocess.run(["java", "-jar", "../flink-project/target/flink-project-1.0-SNAPSHOT.jar", ddl], check=True)
