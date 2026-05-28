import pydantic
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, udf

# --- PHASE A ---
# Runs in driver
spark = SparkSession.builder.appName("ComplexLogic").getOrCreate()
lookup_table = {"A": 1.1, "B": 1.2, "C": 1.3}

# --- PHASE B ---
# Runs in executor
raw_df = spark.read.parquet("s3://data/events/")
meta_df = spark.createDataFrame([("A", "Premium"), ("B", "Standard")], ["code", "type"])


# --- PHASE C ---
# The actual function runs on the Executors. 
udf("double")
def calculate_markup(price, code):
    multiplier = lookup_table.get(code, 1.0)
    return price * multiplier


# --- PHASE D ---
# Executor
joined_df = raw_df.join(meta_df, raw_df.event_code == meta_df.code)

# --- PHASE E ---
# Executor
final_df = joined_df.withColumn(
    "final_price", calculate_markup("price", "code")
).filter(col("type") == "Premium")

# --- PHASE F ---
# The first part of the aggregations and group by is done by the executors
# and the final aggregations is done by the driver so as the collect.
report = final_df.groupBy("type").agg(avg("final_price")).collect()

# --- PHASE G ---
# Runs in driver
for row in report:
    print(f"Type: {row['type']}, Avg: {row['avg(final_price)']}")
