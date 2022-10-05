import json
import multiprocessing

from datagen import datagenerator, utils


def create_files(path, count, full_filenames, schema, lines, processes):
    iterable = [(path, full_filenames[i], schema, lines) for i in range(count)]

    with multiprocessing.Pool(processes=processes) as pool:
        print('generating data...')
        pool.map(create_file, iterable, utils.files_per_process(count, processes))
        print('finished data generation')


def create_file(args):
    path, full_filename, schema, lines = args
    with open(f'{path}/{full_filename}', 'w') as data_file:
        for _ in range(lines):
            data = datagenerator.generate_data(schema)
            json.dump(data, data_file)
            data_file.write('\n')
