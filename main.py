from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col

from protodf import schema_for, message_to_row


def specific_message_bytes_to_row(pb_bytes):
    # import your protobuf here
    msg = message_type.FromString(pb_bytes)
    row = message_to_row(message_type().DESCRIPTOR, msg)
    return row


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("StructuredProtobuf") \
        .getOrCreate()

    message_type = {}  # TODO: replace with a specific Protobuf message

    schema = schema_for(message_type().DESCRIPTOR)

    specific_message_bytes_to_row_udf = udf(specific_message_bytes_to_row, schema)

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "topic") \
        .load()

    df = df.withColumn("event", specific_message_bytes_to_row_udf(col("value")))

    df.printSchema()

    # Now you can query your protobuf with regular SQL! Nested messages, repeated, etc are all supported!

    df = df.select("event.field_name", "event.nested_message.field")

    query = df.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", "false") \
        .start()

    query.awaitTermination()
