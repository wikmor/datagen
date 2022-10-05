from datagen import argparser, configuration


def test_args():
    args = argparser.get_args(configuration.get_config_defaults(), ['--count=2', '--filename=mydata'])
    assert args.count == 2
    assert args.filename == "mydata"
