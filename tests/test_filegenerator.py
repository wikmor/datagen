import os

import pytest

from datagen import filesgenerator


@pytest.fixture
def temporary_path(tmp_path):
    path = tmp_path / "temp_data"
    path.mkdir()
    for i in range(2):
        file = path / f"superdata_{i}.json"
        file.write_text('{}')
    return path


def test_create_file(temporary_path):
    args = temporary_path, "superdata_0.json", {"name": "str:Jorge", "age": "int:25"}, 1
    filesgenerator.create_file(args)
    file = temporary_path / "superdata_0.json"
    assert file.read_text() == '{"name": "Jorge", "age": 25}\n'


def test_create_files(temporary_path):
    full_filenames = ["superdata_0.json", "superdata_1.json"]
    filesgenerator.create_files(temporary_path, 2, full_filenames, {"name": "str:Jorge", "age": "int:25"}, 10, 1)
    file1 = temporary_path / "superdata_0.json"
    file2 = temporary_path / "superdata_1.json"
    assert file1.read_text() == '{"name": "Jorge", "age": 25}\n' * 10
    assert file2.read_text() == '{"name": "Jorge", "age": 25}\n' * 10


@pytest.fixture
def full_filenames():
    return [f"superdata_{i}.json" for i in range(100)]


def test_number_of_lines(tmpdir, full_filenames):
    filesgenerator.create_files(tmpdir, count=100, full_filenames=full_filenames, schema={"age": "int:50"}, lines=10,
                                processes=32)
    for i in range(100):
        with open(f'{tmpdir}/superdata_{i}.json') as data_file:
            lines = data_file.readlines()
            assert len(lines) == 10


def test_number_of_created_files(tmpdir, full_filenames):
    assert len(os.listdir(tmpdir)) == 0
    filesgenerator.create_files(path=tmpdir, count=100, full_filenames=full_filenames, schema={"name": "str:Bob"},
                                lines=10, processes=4)
    assert len(os.listdir(tmpdir)) == 100
