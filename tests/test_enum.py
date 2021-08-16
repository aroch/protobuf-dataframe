import pytest
from protodf import schema_for, message_to_row, ProtoDfError

from .contracts.example_pb2 import ContractWithEnum, NestedContract


@pytest.mark.parametrize("name,number", [("Second", 1), ("Fourth", 3)])
def test_creates_row_with_enum_name_and_value(name, number):
    # Arrange
    instance = NestedContract() # Contract with enum property
    instance.id = ""
    instance.my_enum = number
    bytes = instance.SerializeToString()
    msg = NestedContract.FromString(bytes)

    # Act
    row = message_to_row(NestedContract().DESCRIPTOR, msg)

    # Assert
    assert row.my_enum == {"name": name, "number": number}


def test_raises_proto_df_error_when_enum_number_does_not_exist():
    # Arrange
    instance = NestedContract() # Contract with enum property
    instance.my_enum = 2 # None existing enum number
    bytes = instance.SerializeToString()
    msg = NestedContract.FromString(bytes)

    # Act and assert
    with pytest.raises(ProtoDfError):
        message_to_row(NestedContract().DESCRIPTOR, msg)
