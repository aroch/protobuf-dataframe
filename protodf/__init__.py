from pyspark.sql.types import Row, StringType, StructType, LongType, DoubleType, FloatType, IntegerType, \
    BooleanType, BinaryType, ArrayType

possible_types = {
    1: lambda t: DoubleType(),
    2: lambda t: FloatType(),
    3: lambda t: LongType(),
    4: lambda t: LongType(),
    5: lambda t: IntegerType(),
    8: lambda t: BooleanType(),
    9: lambda t: StringType(),
    11: lambda t: schema_for(t.message_type),
    12: lambda t: BinaryType(),
    13: lambda t: LongType(),
    14: lambda t: StringType()  # enum type
}


def schema_for(descriptor):
    if descriptor is None:
        return None

    struct_type = StructType()

    for field_descriptor in descriptor.fields:
        struct_type.add(
            field_descriptor.name,
            __type_for(field_descriptor),
            field_descriptor.label != field_descriptor.LABEL_REPEATED and
            field_descriptor.label != field_descriptor.LABEL_REQUIRED
        )

    return struct_type


def __type_for(field_descriptor):
    get_type = possible_types.get(field_descriptor.type, lambda t: StringType())
    if field_descriptor.label == field_descriptor.LABEL_REPEATED:
        return ArrayType(get_type(field_descriptor))
    return get_type(field_descriptor)


def message_to_row(descriptor, message):
    field_map = {}
    for field_tuple in message.ListFields():
        field_map[field_tuple[0].name] = field_tuple[1]

    values = []

    for field_descriptor in descriptor.fields:
        if field_descriptor.name in field_map:
            if field_descriptor.label == field_descriptor.LABEL_REPEATED:
                values.append([__to_row_data(field_descriptor, data) for data in
                               field_map[field_descriptor.name]])
            else:
                values.append(__to_row_data(field_descriptor, field_map[field_descriptor.name]))
        else:
            values.append(None)

    return Row(*values)


def __to_row_data(field_descriptor, data):
    if field_descriptor.message_type is not None:
        return message_to_row(field_descriptor.message_type, data)
    if field_descriptor.type == field_descriptor.TYPE_ENUM:
        return field_descriptor.enum_type.values[data].name
    return data
