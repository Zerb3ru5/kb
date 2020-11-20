from click import secho
from tabulate import tabulate
import sys
from datetime import date, datetime
from kb.util.default_values import DATABASE_PATH
import traceback


def output_parse(func):
    def wrapper(*args, **kwargs):
        out = func(*args, **kwargs)

        # if there was an error
        if out['code'] == 1:
            # error handling
            secho('\nError: ' + out['return'], fg='red')
            sys.exit()

        # a normal output of the application
        elif out['code'] == 2:
            secho('\n' + out['return'], fg='green')

        # no output required, pass the return value on
        elif out['code'] == 0:
            return out['return']

    return wrapper


def to_table(data, header):
    return tabulate(tabular_data=data, headers=header, tablefmt='simple', stralign='right')


def to_list(data):
    return tabulate(tabular_data=data, tablefmt='simple', stralign='left')
