import sys

from pywal.backends import (
    colorthief,
    colorz,
    fast_colorthief,
    haishoku,
    schemer2,
    wal,
)

if __name__ == "__main__" and len(sys.argv) > 1:
    print(
        {
            "colorthief": colorthief.get,
            "colorz": colorz.get,
            "fast_colorthief": fast_colorthief.get,
            "haishoku": haishoku.get,
            "schemer2": schemer2.get,
            "wal": wal.get,
        }[sys.argv[1]](sys.argv[2], sys.argv[3] == "1" if len(sys.argv) > 3 else False)
    )
