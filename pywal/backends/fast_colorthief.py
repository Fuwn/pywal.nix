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
Generate a colorscheme using fast_colorthief.
"""

import logging
import sys

try:
    import fast_colorthief

except ImportError:
    logging.error("fast_colorthief wasn't found on your system.")
    logging.error("Try another backend. (wal --backend)")
    sys.exit(1)

from .. import util


def gen_colors(img):
    """Ask backend to generate 16 colors."""
    raw_colors = fast_colorthief.get_palette(img, 16)

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
