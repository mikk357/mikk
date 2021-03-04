import os
import random
from argparse import ArgumentParser
from pathlib import Path


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

parser.add_argument(
    "--ext",
    dest="exts",
    help="filter by extensions (sample: `--ext mp3,m4a,opus`)",
    required=False,
    nargs="?",
    type=(lambda s: s.split(",")),
    default=[],
)

parser.add_argument(
    "--then",
    dest="action",
    help="action with file (sample: `--then \"move {} trash\"`)",
    required=False,
    nargs="?",
    type=str,
    default=None,
)


def main():
    cwd = Path.cwd().resolve()

    args = parser.parse_args()
    extensions = {f"{os.extsep}{i}" for i in args.exts.copy()}

    if extensions:
        def filefilter(file: Path):
            return file.is_file() and file.suffix in extensions
    else:
        def filefilter(file: Path):
            return file.is_file()

    _glob = (cwd.rglob("*.*") if args.deep else cwd.glob("*.*"))

    files = list(filter(filefilter, _glob))

    if files:
        file = random.choice(files)
        string = str(file).replace(str(cwd), ".", 1)  # 'relative' path
        print(f"\"{string}\"")
        if args.action is not None:
            cmd = args.action.replace("{}", f"\"{string}\"")
            os.system(cmd)
        return 0
    else:
        print("not finded any files")
        return 1


if __name__ == '__main__':
    exit(main())
