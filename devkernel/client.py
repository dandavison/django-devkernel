import json
import os
import sys

from jupyter_client import BlockingKernelClient
from jupyter_client import find_connection_file


def execute_from_command_line():
    if sys.argv.count('--existing') != 1:
        raise ValueError(f'{sys.argv}\n'
                         f'--existing argument must occur once only.')

    kernel_arg_index = sys.argv.index('--existing')
    try:
        kernel_name = sys.argv[kernel_arg_index + 1]
    except IndexError:
        # Following the command-line API of jupyter console, qtconsole etc, the --existing argument
        # can be used without a value, meaning use the kernel whose connection file has most
        # recently been accessed. We support that here when --existing is the last element of the
        # command line. Otherwise, the behavior of the no-argument-value form can be achieved with
        # --existing ''.
        kernel_name = None
    else:
        sys.argv.pop(kernel_arg_index + 1)

    sys.argv.pop(kernel_arg_index)

    if {'shell', 'shell_plus'} & set(sys.argv):
        # Special case: use `jupyter console` for management commands requesting a python shell.
        argv = ['jupyter', 'console', '--Completer.use_jedi=False', '--existing']
        if kernel_name:
            argv.append(kernel_name)
        os.execlp(argv[0], *argv)

    connection_file = find_connection_file(kernel_name) if kernel_name else find_connection_file()
    kernel_client = BlockingKernelClient(connection_file=connection_file)
    kernel_client.load_connection_file()
    response = kernel_client.execute_interactive(f"""
from devkernel.kernel import execute_from_command_line
execute_from_command_line('{json.dumps(sys.argv)}')
""")
    exit_status = 0 if response['metadata']['status'] == 'ok' else 1
    sys.exit(exit_status)
