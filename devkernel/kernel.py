import json
import sys
from contextlib import contextmanager
from contextlib import ExitStack
from importlib import reload
from unittest import mock

from django.core.management import execute_from_command_line as django_execute_from_command_line
from devkernel.color import red


def execute_from_command_line(argv):
    argv = json.loads(argv)

    if '--reload-modules' in argv:
        reload_modules(argv)
        if not argv:
            return

    with apply_patches(argv):
        return django_execute_from_command_line(argv)


def reload_modules(argv):
    reload_modules_index = argv.index('--reload-modules')
    modules_to_reload = argv.pop(reload_modules_index + 1).split(',')
    argv.pop(reload_modules_index)
    print(f'Reloading modules: {", ".join(modules_to_reload)}')
    for name in modules_to_reload:
        module = sys.modules.get(name)
        if not module:
            print(red(f'Warning: module {name} is not in sys.modules'), file=sys.stderr)
        else:
            reload(module)


@contextmanager
def apply_patches(argv):
    # nose requires that the argv passed to execute_from_command_line matches sys.argv,
    # so if nose is bneing used then this is necessary for manage.py test, at least.
    inherit_sys_argv_from_client = mock.patch.object(sys, 'argv', argv)

    patches = [inherit_sys_argv_from_client]

    try:
        from django_nose.plugin import DjangoSetUpPlugin
    except ImportError:
        pass
    else:
        # For `manage.py test`, we don't want DjangoSetUpPlugin to setup and teardown.
        def disable_plugin(self, *args, **kwargs):
            self.enabled = False

        disable_django_setup_plugin = (mock.patch
                                       .object(DjangoSetUpPlugin, 'configure', disable_plugin))
        patches.append(disable_django_setup_plugin)

    with ExitStack() as stack:
        yield [stack.enter_context(patch) for patch in patches]
