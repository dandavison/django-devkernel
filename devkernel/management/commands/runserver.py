from django.core.management.commands import runserver

import devkernel.autoreload


class DevkernelRunserverMixin:

    def add_arguments(self, parser):
        parser.add_argument(
            '--kernel',
            action='store_true', dest='start_kernel', default=False,
            help='Start a Jupyter Python kernel in the server process.',
        )
        super().add_arguments(parser)

    def run(self, **options):
        start_kernel = options.pop('start_kernel')
        if not start_kernel:
            super().run(**options)
        else:
            assert options['use_reloader'], '--kernel cannot be used with --noreload'
            devkernel.autoreload.run_with_reloader(self.inner_run, **options)


class Command(DevkernelRunserverMixin, runserver.Command):
    pass
