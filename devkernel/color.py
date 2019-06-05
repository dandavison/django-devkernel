from functools import partial

from django.utils.termcolors import colorize


def blue(string, bold=False):
    return _get_colorizer('blue', bold)(string)


def cyan(string, bold=False):
    return _get_colorizer('cyan', bold)(string)


def green(string, bold=False):
    return _get_colorizer('green', bold)(string)


def magenta(string, bold=False):
    return _get_colorizer('magenta', bold)(string)


def red(string, bold=False):
    return _get_colorizer('red', bold)(string)


def white(string, bold=False):
    return _get_colorizer('white', bold)(string)


def yellow(string, bold=False):
    return _get_colorizer('yellow', bold)(string)


def black(string, bold=False):
    return _get_colorizer('black', bold)(string)


def _get_colorizer(color, bold):
    opts = []
    if bold:
        opts.append('bold')
    return partial(colorize, fg=color, opts=opts)
