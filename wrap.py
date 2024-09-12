import sys

from pywal.backends import (
    colorthief,
    colorz,
    wal,
)

if __name__ == "__main__" and len(sys.argv) > 1:
    print(
        {
            "colorthief": colorthief.get,
            "colorz": colorz.get,
            "wal": wal.get,
        }[
            sys.argv[1]
        ](sys.argv[2], sys.argv[3] == "1" if len(sys.argv) > 3 else False)
    )
