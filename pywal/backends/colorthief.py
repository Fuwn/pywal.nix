# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Generate a colorscheme using ColorThief.
"""

import logging
import sys

try:
    from colorthief import ColorThief

except ImportError:
    logging.error("ColorThief wasn't found on your system.")
    logging.error("Try another backend. (wal --backend)")
    sys.exit(1)

from .. import util


def gen_colors(img):
    """Loop until 16 colors are generated."""
    color_cmd = ColorThief(img).get_palette

    for i in range(0, 10, 1):
        raw_colors = color_cmd(color_count=8 + i)

        if len(raw_colors) >= 8:
            break

        if i == 10:
            logging.error("ColorThief couldn't generate a suitable palette.")
            sys.exit(1)

    return [util.rgb_to_hex(color) for color in raw_colors]


def adjust(cols, light):
    """Create palette."""
    cols.sort(key=util.rgb_to_yiq)
    raw_colors = [*cols, *cols]

    if light:
        raw_colors[0] = util.lighten_color(cols[0], 0.90)
        raw_colors[7] = util.darken_color(cols[0], 0.75)

    else:
        for color in raw_colors:
            color = util.lighten_color(color, 0.40)

        raw_colors[0] = util.darken_color(cols[0], 0.80)
        raw_colors[7] = util.lighten_color(cols[0], 0.60)

    raw_colors[8] = util.lighten_color(cols[0], 0.20)
    raw_colors[15] = raw_colors[7]

    return raw_colors


def get(img, light=False):
    """Get colorscheme."""
    cols = gen_colors(img)
    return adjust(cols, light)
