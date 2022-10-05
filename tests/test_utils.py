import os

import pytest

from datagen import utils

SCHEMA = '{"name": "str:rand"}'


def test_getting_schema_file(tmp_path):
    d = tmp_path / "test_schemas"
    d.mkdir()
    p = d / "test_schema.json"
    p.write_text(SCHEMA)
    assert utils.get_schema(p.read_text()) == {"name": "str:rand"}


def test_getting_schema_cli():
    assert utils.get_schema('{"name": "str:rand"}') == {"name": "str:rand"}


@pytest.fixture
def temporary_path(tmp_path):
    path = tmp_path / "temp_data"
    path.mkdir()
    for i in range(2):
        file = path / f"superdata_{i}.json"
        file.write_text('{"date": "timestamp:"}')
    return path


def test_clear(temporary_path):
    assert len(os.listdir(temporary_path)) == 2
    utils.clear_files(temporary_path, "superdata")
    assert len(os.listdir(temporary_path)) == 0


invalid_data_schemas = ['{"random_number"="int:rand(0, 10)"}',
                        '{"name"="str:Patrick"}']


@pytest.mark.parametrize('schema', invalid_data_schemas)
def test_getting_invalid_schemas_cli(schema, caplog):
    with pytest.raises(SystemExit):
        utils.get_schema(schema)
    assert "in schema - expecting property name enclosed in double quotes\n" in caplog.text


def test_invalid_number_of_processes(caplog):
    with pytest.raises(SystemExit):
        utils.get_number_of_processes(0)
    assert 'number of processes must be at least 1' in caplog.text


def test_processes_more_than_os():
    number_of_processes = utils.get_number_of_processes(1000)
    assert number_of_processes == os.cpu_count()


def test_files_per_process():
    number_of_files = utils.files_per_process(100, 4)
    assert number_of_files == (100 // 4) + 1


def test_files_per_process_else():
    number_of_files = utils.files_per_process(3, 4)
    assert number_of_files == 1


def test_getting_full_filename():
    full_filename = utils.get_full_filename(2, "superdata", '0')
    assert full_filename == "superdata_0.jsonl"


def test_getting_filename():
    full_filename = utils.get_full_filename(1, "superdata", '0')
    assert full_filename == "superdata.jsonl"
