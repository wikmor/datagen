import json
import os
import random
import uuid

from datagen import logger


def get_path(path):
    if os.path.exists(path) and not os.path.isdir(path):
        logger.error(f'path {path} exists, but is not a directory')

    os.makedirs(path, exist_ok=True)
    return path


def get_full_filename(count, filename, suffix):
    """Get full filename, no need to check count < 1, because handled before in the code"""
    if count > 1:
        return f'{filename}_{suffix}.jsonl'

    return f'{filename}.jsonl'


def get_suffix(count, suffix, i):

    # No duplications
    if suffix == 'count':
        return str(i)

    # Duplicates can occur, but the chance is low
    elif suffix == 'random':
        return str(random.randrange(count * 100_000))

    # Chance for duplication is nearly zero
    else:
        return str(uuid.uuid4())


def get_schema(schema: str) -> dict:
    """Get data schema by path to file or string"""
    if schema[-5:] == '.json':
        if os.path.exists(schema) and os.path.isfile(schema):
            with open(schema) as schema_file:
                schema = json.load(schema_file)
        else:
            logger.error('path to schema is not valid')
    else:
        try:
            schema = json.loads(schema)
        except json.decoder.JSONDecodeError:
            logger.error('in schema - expecting property name enclosed in double quotes')

    return schema


def clear_files(path, filename):
    """Delete all files in path that match filename"""
    files = os.listdir(path)
    for file in files:
        if file.startswith(filename):
            os.remove(f'{path}/{file}')


def get_number_of_processes(processes):
    if processes < 1:
        logger.error('number of processes must be at least 1')

    if processes > os.cpu_count():
        processes = os.cpu_count()

    return processes


def files_per_process(count, processes):
    # Divide files count to equal chunks
    # All taskels need (almost) exactly the same computation time [taskel = task + element]
    if count > processes:
        # Dense Scenario? For maximal throughput, we want all worker processes busy until all tasks are processed
        # (no idling workers). For this goal, the distributed chunks should be of equal size or close to.
        # https://stackoverflow.com/questions/53751050/multiprocessing-understanding-logic-behind-chunksize
        return (count // processes) + 1

    else:
        return 1
