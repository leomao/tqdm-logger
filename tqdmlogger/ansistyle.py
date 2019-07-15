# /usr/bin/env python

# Copyright (C) 2017 Leo Mao

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

ESC = '\x1b['
END = 'm'

ATTRIBUTES = {
    'bold':         1,
    'dim':          2,
    'italic':       3,
    'underlined':   4,
    'blink':        5,
    'reverse':      7,
    'conceal':      8,
    'no_bold':     21,
    'no_bold_dim': 22,
    'no_italic':   23,
    'no_underline':24,
    'no_blink':    25,
    'no_reverse':  27,
    'no_conceal':  28,
}

ATTR_CODES = set(ATTRIBUTES.values())

COLOR_NAMES = {
    'black':         0,
    'red':           1,
    'green':         2,
    'yellow':        3,
    'blue':          4,
    'magenta':       5,
    'cyan':          6,
    'light_gray':    7,
    'dark_gray':     8,
    'light_red':     9,
    'light_green':   10,
    'light_yellow':  11,
    'light_blue':    12,
    'light_magenta': 13,
    'light_cyan':    14,
    'white':         15,
}

RESET = '{}{}{}'.format(ESC, 0, END)

HEX_RE = r'#[0-9a-f]{6}'
HEXCODE_RE = r'[0-9a-f]{2}'

def _256_code(n):
    return '5;{}'.format(n)

def _tuple_code(t):
    return '2;{};{};{}'.format(*t)

def validate_color(c):
    try:
        tp = type(c)
        if tp is str:
            c = c.lower()
            if c in COLOR_NAMES:
                return _256_code(COLOR_NAMES[c])
            elif re.fullmatch(HEX_RE, c):
                return _tuple_code(int(x, base=16)
                                   for x in re.findall(HEXCODE_RE, c[1:]))
        elif tp is int:
            if c >= 0 and c <= 255:
                return _256_code(c)
        elif tp is tuple or tp is list and len(c) == 3:
            if all(x >= 0 and x <= 255 for x in c):
                return _tuple_code(c)
    except TypeError:
        pass
    raise TypeError('The format of the color is incorrect.')

def fg(c):
    return ''.join((ESC, '38;', validate_color(c), END))

def bg(c):
    return ''.join((ESC, '48;', validate_color(c), END))

def attr(at):
    if at in ATTRIBUTES:
        return '{}{}{}'.format(ESC, ATTRIBUTES[at], END)
    elif at in ATTR_CODES:
        return '{}{}{}'.format(ESC, at, END)
    else:
        raise TypeError("The attribute `{}` doens't exist.".format(s))

def stylize(text, *styles, reset=True):
    term = RESET if reset else ''
    return '{}{}{}'.format(''.join(styles), text, term)

if __name__ == '__main__':
    # simple test as example
    for i in range(256):
        print(stylize('TEXT', fg(i)))

    print(stylize('TEXT', fg(123), bg('#AE01b2')))
    print(stylize('TEXT', fg(223), bg('#0E01b2'), attr('bold')))
    print(stylize('TEXT', fg(23), bg((100, 100, 100)), attr(4)))
