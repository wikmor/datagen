import ast
import random
import time
import uuid

from datagen import logger


def generate_data(schema: dict) -> dict:
    """Generate test data based on schema according to Data Schema Parse point"""
    data = {}

    for key, value in schema.items():
        left, right = value.split(':')

        # Check if value type is valid
        if left not in ['timestamp', 'str', 'int']:
            logger.error('available value types are timestamp, str and int')

        # Logic for timestamp value type
        elif left == 'timestamp':
            if right:
                logger.warn('timestamp does not support any values')
            data[key] = time.time()

        # Logic if right part of value does not exist
        elif not right:
            if left == 'int':
                data[key] = None
            elif left == 'str':
                data[key] = ''

        # Logic for right part of value
        elif right == 'rand':
            if left == 'str':
                data[key] = str(uuid.uuid4())
            elif left == 'int':
                data[key] = random.randint(0, 10_000)

        elif right[0] == '[' and right[-1] == ']':
            str_or_int_list = ast.literal_eval(right)
            data[key] = random.choice(str_or_int_list)

        elif right[:5] == 'rand(':
            if left == 'int':
                rand_range = right[5:-1].split(', ')
                rand_from = int(rand_range[0])
                rand_to = int(rand_range[1])
                data[key] = random.randint(rand_from, rand_to)
            else:
                logger.error('random int values generation cannot be of str or timestamp type')

        elif right and left == 'int':
            try:
                integer = ast.literal_eval(right)
                if type(integer).__name__ == left:
                    data[key] = int(integer)
            except ValueError:
                logger.error(f'{right} cannot be converted to {left}')

        else:
            data[key] = right

    return data
