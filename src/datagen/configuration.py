import configparser


def get_config_defaults() -> configparser.SectionProxy:
    """Create default.ini configuration file and get DEFAULT section"""
    config = configparser.ConfigParser()
    config.read('src/datagen/default.ini')

    return config['DEFAULT']
