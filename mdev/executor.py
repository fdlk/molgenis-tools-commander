import configparser

from mdev import history, io
from mdev.utils import MdevError


def execute(args, exit_on_error, arg_string):
    try:
        args.func(args)
    except MdevError as e:
        _handle_error(str(e), args.write_to_history, arg_string, exit_on_error)
    except configparser.Error as e:
        message = 'Error reading or writing mdev.properties: %s' % str(e)
        _handle_error(message, args.write_to_history, arg_string, exit_on_error)
    else:
        if args.write_to_history:
            history.write(arg_string, success=True)
        io.succeed()


def _handle_error(message, write_to_history, arg_string, exit_on_error):
    io.error(message)
    if write_to_history:
        history.write(arg_string, success=False)
    if exit_on_error:
        exit(1)