import importlib
import sys

if __name__ == "__main__" and len(sys.argv) > 1:
    backend = importlib.import_module(f"pywal.backends.{sys.argv[1]}")
    light = sys.argv[3] == "1" if len(sys.argv) > 3 else False

    print(backend.get(sys.argv[2], light))
