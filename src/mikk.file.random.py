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
    "--rel",
    dest="relative",
    help="try to make a path relative",
    required=False,
    action="store_true",
    default=False
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


def main() -> int:
    cwd = Path.cwd().resolve()

    args = parser.parse_args()
    extensions = {f"{os.extsep}{i}" for i in args.exts.copy()}

    iglob = (
        i
        for i in (cwd.rglob("*") if args.deep else cwd.glob("*"))
        if i.is_file()
    )

    if extensions:
        files = tuple(i for i in iglob if i.suffix in extensions)
    else:
        files = tuple(iglob)

    if files:
        file = random.choice(files)

        if args.relative:
            string = str(file.relative_to(cwd))
        else:
            string = str(file)

        if args.action is not None:
            cmd = args.action.replace("{}", f"\"{string}\"")
            os.system(cmd)
        else:
            print(string)

        return 0

    else:
        print("not finded any files")
        return 1


if __name__ == '__main__':
    exit(main())
