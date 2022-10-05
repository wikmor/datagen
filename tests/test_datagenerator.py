import uuid

import pytest

from datagen import datagenerator

invalid_data_types = [
    ({"number": "str:rand(1, 2)"}, "random int values generation cannot be"),
    ({"tuple": "tuple:(test, tuple)"}, "available value types are timestamp, str and int"),
    ({"list": "list:[1, 2, 3]"}, "available value types are timestamp, str and int"),
    ({"age": "int:head"}, "cannot be converted to")
]


@pytest.mark.parametrize('schema, message', invalid_data_types)
def test_invalid_data_types(schema, message, caplog):
    with pytest.raises(SystemExit):
        datagenerator.generate_data(schema)
    assert message in caplog.text


valid_schema = {"type": 31,
                "name": "test",
                "name_test": "test",
                "name_null": "",
                "int_null": None,
                "integer": 31}


def test_valid_schema():
    assert datagenerator.generate_data({"type": "int:[31]",
                                        "name": "str:['test']",
                                        "name_test": "str:test",
                                        "name_null": "str:",
                                        "int_null": "int:",
                                        "integer": "int:31"}) == valid_schema


def test_timestamp_warn():
    with pytest.warns(UserWarning):
        datagenerator.generate_data({"date": "timestamp:value"})


def test_random_type_str():
    generated_data = datagenerator.generate_data({"name": "str:rand"})
    uuid_to_test = generated_data["name"]
    uuid_obj = uuid.UUID(uuid_to_test, version=4)
    assert str(uuid_obj) == uuid_to_test


def test_random_type_int():
    generated_data = datagenerator.generate_data({"number": "int:rand"})
    number_to_test = generated_data["number"]
    assert number_to_test in range(0, 10_001)


def test_random_range():
    generated_data = datagenerator.generate_data({"number": "int:rand(0, 10)"})
    number_to_test = generated_data["number"]
    assert number_to_test in range(0, 11)
