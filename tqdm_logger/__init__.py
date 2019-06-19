import shutil
import sys
import logging
import datetime
from collections.abc import Sequence

# must import before import tqdm
import tqdm._utils as tqdm_utils
from tqdm import tqdm
from .ansistyle import stylize, fg, bg, attr, RESET


def _get_cols():
    return shutil.get_terminal_size().columns


class DummyTqdmFile:
    MOVE_UP = tqdm_utils._term_move_up()

    def __init__(self, fobj):
        self.fobj = fobj
        self._updating = False
        self.tmp_cnt = 0
        self.line_cnt = 0
        self.open_bar = None

    def updating(self):
        self.tmp_cnt = 0
        self._updating = True

    def updated(self):
        self._updating = False
        self.line_cnt = self.tmp_cnt

    def flush(self):
        self.line_cnt = 0

    def write(self, msg):
        tqdm_instances = getattr(tqdm, '_instances', [])
        # find the most outer instance
        outer_bar = None
        pos = len(tqdm_instances)
        for inst in tqdm_instances:
            if abs(inst.pos) <= pos:
                outer_bar = inst

        # check if the previous open instance is closed.
        if self.open_bar is not None:
            if self.open_bar not in tqdm_instances:
                self.line_cnt = 0
        self.open_bar = outer_bar

        # record line count if we are printing refreshable messages
        if self._updating:
            self.tmp_cnt += msg.count('\n')
            if self.line_cnt > 0:
                msg = DummyTqdmFile.MOVE_UP * self.line_cnt + msg

        cols = _get_cols()
        msg = msg.rstrip().ljust(cols)

        self.line_cnt = 0
        if msg.rstrip():
            tqdm.write(msg, file=self.fobj)
        self.fobj.flush()


class Formatter(logging.Formatter):
    def __init__(self):
        super().__init__(fmt=None,
                         datefmt='%H:%M:%S',
                         style='{')
        self._high_precision = False
        self.set_time_mode()

    def set_time_mode(self, mode='both'):
        if mode == 'delta':
            self._fmt = 'Δ {timedelta} - {message}'
        elif mode == 'time':
            self._fmt = '{asctime} - {message}'
        elif mode == 'both':
            self._fmt = '{asctime} Δ {timedelta} - {message}'
        # hack the formatter internal implementation
        self._style._fmt = self._fmt

    def set_high_precision(self, flag):
        self._high_precision = flag

    def format_timedelta(self, delta):
        if self._high_precision:
            delta = datetime.timedelta(milliseconds=delta)
        else:
            delta = datetime.timedelta(seconds=int(delta / 1000))
        return str(delta)

    def format(self, record):
        record.timedelta = self.format_timedelta(record.relativeCreated)
        return super().format(record)


_output_fp = DummyTqdmFile(sys.stderr)
_formatter = Formatter()

_handler = logging.StreamHandler(_output_fp)
_handler.setFormatter(_formatter)
_handler.setLevel(logging.INFO)

logger = logging.getLogger()
logger.addHandler(_handler)


def set_high_precision(flag=True):
    _formatter.set_high_precision(flag)


def set_time_mode(mode='time'):
    _formatter.set_time_mode(mode)


def atten(*args):
    return stylize(' '.join(str(x) for x in args), fg('red'), attr('bold'))


def note(*args):
    return stylize(' '.join(str(x) for x in args), fg('yellow'),
                   attr('underlined'))


def section_prefix(text, color=None):
    if color is None:
        return '[{}]'.format(text)
    else:
        return '{}[{}]{}'.format(fg(color), text, RESET)


def flush():
    _output_fp.flush()


def log(*args, attrs=None, prefix=None, update=False):
    msg = ' '.join(str(x) for x in args)
    if attrs:
        styles = (attr(s) for s in attrs)
        msg = stylize(msg, *styles)

    if update:
        _output_fp.updating()

    for line in msg.split('\n'):
        if prefix:
            line = '{} {}'.format(prefix, line)
        logger.warning(line)

    if update:
        _output_fp.updated()


def seclog(section, *args, attrs=None, update=False):
    if isinstance(section, str):
        section = section_prefix(section)
    elif isinstance(section, Sequence):
        section = section_prefix(*section)
    else:
        raise TypeError('the type of section is wrong!')
    log(*args, attrs=attrs, prefix=section, update=update)
    return section


def warning(*args):
    log(atten('[Warning]'), *args)


__all__ = [
    'atten',
    'note',
    'log',
    'seclog',
    'warning',
    'logger',
    'set_high_precision',
    'set_time_mode',
]
