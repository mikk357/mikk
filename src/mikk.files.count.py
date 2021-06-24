import os
from pathlib import Path


def main():
    cwd = Path.cwd().resolve()
    count = 0

    for _, _, f in os.walk(cwd):
        count += len(f)

    print(f"\t{count} files")


if __name__ == '__main__':
    main()
