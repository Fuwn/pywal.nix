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
Generate a colorscheme using Schemer2.
"""

import logging
import shutil
import subprocess
import sys

from .. import colors
from .. import util


def gen_colors(img):
    """Generate a colorscheme using Colorz."""
    cmd = ["schemer2", "-format", "img::colors", "-minBright", "75", "-in"]
    return subprocess.check_output([*cmd, img]).splitlines()


def adjust(cols, light):
    """Create palette."""
    cols.sort(key=util.rgb_to_yiq)
    raw_colors = [*cols[8:], *cols[8:]]

    return colors.generic_adjust(raw_colors, light)


def get(img, light=False):
    """Get colorscheme."""
    if not shutil.which("schemer2"):
        logging.error("Schemer2 wasn't found on your system.")
        logging.error("Try another backend. (wal --backend)")
        sys.exit(1)

    cols = [col.decode("UTF-8") for col in gen_colors(img)]
    return adjust(cols, light)
