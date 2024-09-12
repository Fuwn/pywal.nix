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
Generate a colorscheme using Colorz.
"""
import logging
import sys

try:
    import colorz

except ImportError:
    logging.error("colorz wasn't found on your system.")
    logging.error("Try another backend. (wal --backend)")
    sys.exit(1)

from .. import colors
from .. import util


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    # pylint: disable=not-callable
    raw_colors = colorz.colorz(img, n=6, bold_add=0)
    return [util.rgb_to_hex([*color[0]]) for color in raw_colors]


def adjust(cols, light):
    """Create palette."""
    raw_colors = [cols[0], *cols, "#FFFFFF", "#000000", *cols, "#FFFFFF"]

    return colors.generic_adjust(raw_colors, light)


def get(img, light=False):
    """Get colorscheme."""
    cols = gen_colors(img)

    if len(cols) < 6:
        logging.error("colorz failed to generate enough colors.")
        logging.error("Try another backend or another image. (wal --backend)")
        sys.exit(1)

    return adjust(cols, light)
