import optimistic_reload.django
from django.core.management.commands import runserver

import devkernel.autoreload


class DevkernelRunserverMixin:

    def add_arguments(self, parser):
        parser.add_argument(
            '--kernel',
            action='store_true', dest='start_kernel', default=False,
            help='Start a Jupyter Python kernel in the server process.',
        )
        parser.add_argument(
            '--optimistic-reload',
            action='store_true', dest='use_optimistic_reloader', default=False,
            help=('When code is changed on disk, attempt to reload the minimal set of required '
                  'modules, without restarting the server.'),
        )
        super().add_arguments(parser)

    def run(self, **options):
        if options['use_optimistic_reloader']:
            devkernel.autoreload.file_changed.connect(
                optimistic_reload.django.file_changed_signal_handler
            )
        start_kernel = options.pop('start_kernel')
        if not start_kernel:
            super().run(**options)
        else:
            assert options['use_reloader'], '--kernel cannot be used with --noreload'
            if options['use_optimistic_reloader']:
                with optimistic_reload.django.apply_patches():
                    devkernel.autoreload.run_with_reloader(self.inner_run, **options)
            else:
                devkernel.autoreload.run_with_reloader(self.inner_run, **options)


class Command(DevkernelRunserverMixin, runserver.Command):
    pass
