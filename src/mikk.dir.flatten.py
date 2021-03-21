from argparse import ArgumentParser
from pathlib import Path
from typing import Set


parser = ArgumentParser()
parser.add_argument(
    "--deep",
    dest="deep",
    help="scan subdirs",
    required=False,
    action="store_const",
    const=True,
    default=False,
)


def main():
    cwd = Path.cwd().resolve()

    args = parser.parse_args()

    paths = [i for i in cwd.iterdir() if i.is_dir()]

    files: Set[Path] = set()

    for path in paths:
        iglob = (path.rglob("*.*") if args.deep else path.glob("*.*"))
        for some in iglob:
            if some.is_file() and not some.parent == cwd:
                files.add(some)

    for file in files:
        new_path = cwd / file.name
        if new_path.exists():
            print(f"can't move \"{file}\", \"{new_path}\" already exists")
            continue
        try:
            file.rename(new_path)
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")


if __name__ == '__main__':
    exit(main())
