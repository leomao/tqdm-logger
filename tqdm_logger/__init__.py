import logging
import sys

from tqdm import tqdm
from .ansistyle import stylize, fg, bg, attr, RESET

class DummyTqdmFile:
    def __init__(self, fobj):
        self.fobj = fobj

    def write(self, msg):
        if '_instances' not in tqdm.__dict__ or len(tqdm._instances) == 0:
            self.fobj.write(msg)
        elif len(msg.rstrip()) > 0:
            tqdm.write(msg, file=self.fobj)
            self.fobj.flush()

logging.basicConfig(format='{asctime} - {message}',
                    datefmt='%H:%M:%S',
                    style='{',
                    level=logging.INFO,
                    stream=DummyTqdmFile(sys.stderr)
                    )
logger = logging.getLogger('root')


def atten(*args):
    return stylize(' '.join(str(x) for x in args), fg('red'), attr('bold'))


def note(*args):
    return stylize(' '.join(str(x) for x in args), fg('yellow'),
                   attr('underlined'))


def log(*args, attrs=None, prefix=None):
    msg = ' '.join(str(x) for x in args)
    if attrs and len(attrs):
        styles = (attr(s) for s in attrs)
        msg = stylize(msg, *styles)
    for line in msg.split('\n'):
        if prefix:
            line = f'{prefix} {line}'
        logger.warning(line)


def seclog(section, *args, attrs=None):
    if type(section) is list or type(section) is tuple:
        section, color = section
        section = '{}[{}]{}'.format(fg(color), section, RESET)
    log(*args, attrs=attrs, prefix=section)


def warning(*args):
    seclog(atten('[Warning]'), *args)

__all__ = [
    'atten',
    'note',
    'log',
    'seclog',
    'warning',
    'logger',
]
