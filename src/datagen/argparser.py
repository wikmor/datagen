import argparse
import configparser


def get_args(config: configparser.SectionProxy, args: list) -> argparse.Namespace:
    """Create argument parser and get argparse namespace with arguments provided by the user"""
    parser = argparse.ArgumentParser(description='Generate test data based on data schema',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('path', nargs='?', default=config['path'], help='path to save files, "." for cwd')

    parser.add_argument('--count', type=int, default=config['count'], help='files count, ==0: print output to console')

    parser.add_argument('--filename', default=config['filename'], help='with no suffix, full filename="filename.jsonl"')

    parser.add_argument('--suffix', default=config['suffix'], choices=['count', 'random', 'uuid'],
                        help='filename suffix when files count is more than 1, full filename="filename_suffix.jsonl"')

    parser.add_argument('--schema', default=config['schema'], help='path to json file or json string')

    parser.add_argument('--lines', type=int, default=config['lines'], help='number of lines in each file')

    parser.add_argument('--clear', action='store_true', default=bool(config['clear']),
                        help='whether to delete all files in path that match filename')

    parser.add_argument('--multiprocessing', type=int, default=config['multiprocessing'],
                        help='number of processes used to create files')

    return parser.parse_args(args)
