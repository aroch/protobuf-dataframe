## Dependencies
- Create a virtual environment in [PyCharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html) or [CLI](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) 
- Install once by running:
```
pip install -r requirements.txt
```

## Features

- Convert a Protobuf descriptor into a Spark schema:
```
from protodf import schema_for

schema = schema_for(message_type().DESCRIPTOR)
```
- You can use the created schema to transform a Protobuf message from bytes into a Spark Row:

Create a function which your type:

```
from protodf import message_to_row

def specific_message_bytes_to_row(pb_bytes):
    # import your protobuf here
    msg = message_type.FromString(pb_bytes)
    row = message_to_row(message_type().DESCRIPTOR, msg)
    return row
``` 

Turn it into a UDF:
    
```
specific_message_bytes_to_row_udf = udf(specific_message_bytes_to_row, schema)
```

Use the UDF:

```
df = df.withColumn("event", specific_message_bytes_to_row_udf(col("value")))
```

Now you can query your Protobuf with regular SQL! Nested messages, repeated, etc are all supported!

```
df.select("event.field_name", "event.nested_message.field")
```

## Explore the example

In main.py file you would see an example usage for the package 