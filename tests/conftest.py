import os
import pytest
from collections import namedtuple
from pyspark.sql import SparkSession

# Generate Python classes from protobuf messages
os.system('protoc example.proto --python_out contracts  --proto_path contracts')


@pytest.fixture(scope="session")
def spark():
    """ Create Spark Session """
    return SparkSession.builder.appName('SparkByExamples.com').getOrCreate()


@pytest.fixture(scope="session")
def df_factory(spark):
    """ Factory for creating a single row DataFrame from a single binary value """

    def factory(proto_message_bytes):
        """ Based on https://stackoverflow.com/questions/41363296/how-to-store-a-python-bytestring-in-a-spark-dataframe """
        Record = namedtuple("Record", ["raw"])
        rdd = spark.sparkContext.parallelize([Record(proto_message_bytes)])
        df = rdd.map(lambda rec: Record(bytearray(rec.raw))).toDF()
        return df

    return factory
