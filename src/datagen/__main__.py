import sys

from datagen import argparser, configuration, datagenerator, filesgenerator, logger, utils


def main() -> None:
    """Generate JSON test data"""
    config = configuration.get_config_defaults()
    args = argparser.get_args(config, sys.argv[1:])

    count = args.count
    schema = utils.get_schema(args.schema)
    lines = args.lines

    if count < 0:
        logger.error('count must be at least 0')

    # Print output to console
    elif count == 0:
        for i in range(lines):
            print(f'{i+1}. {datagenerator.generate_data(schema)}')

    # Create files, use multiprocessing
    else:
        path = utils.get_path(args.path)
        filename = args.filename
        suffixes = [utils.get_suffix(count, args.suffix, i) for i in range(count)]
        full_filenames = [utils.get_full_filename(count, filename, suffixes[i]) for i in range(count)]
        clear = args.clear
        processes = utils.get_number_of_processes(args.multiprocessing)

        if clear:
            utils.clear_files(path, filename)

        filesgenerator.create_files(path, count, full_filenames, schema, lines, processes)


if __name__ == '__main__':
    main()
