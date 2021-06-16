from argparse import ArgumentParser, Namespace
from typing import List, Dict
from pathlib import Path
import hashlib


argparser = ArgumentParser()
argparser.add_argument(
    "--deep",
    default=False,
    action="store_true",
    help="recursive file scan",
)
argparser.add_argument(
    "--quick",
    default=False,
    action="store_true",
    help="read x<=1MB of file to hash",
)


class Args(Namespace):
    deep: bool
    quick: bool


CHINK_SIZE = 8388608  # 8MB


def filehash(file: Path, args: Args) -> str:
    _hash = hashlib.sha256()
    with file.open("rb") as fh:
        if args.quick:
            _hash.update(fh.read(1024 * 1024))  # 1 MB
            return _hash.hexdigest()
        while True:
            chunk = fh.read(CHINK_SIZE)
            if not chunk:
                break
            _hash.update(chunk)
    return _hash.hexdigest()


def gather(cwd: Path, args: Args) -> Dict[str, List[Path]]:
    mapped: Dict[str, List[Path]] = dict()
    glob_ = (cwd.rglob("*") if args.deep else cwd.glob("*"))
    gen = (i for i in glob_ if i.is_file())
    count = 0

    for file in gen:
        print(f"[{count: >8} files]", end="\r")
        hash_hex = filehash(file, args)
        if hash_hex in mapped:
            mapped[hash_hex].append(file)
        else:
            mapped[hash_hex] = [file]
        count += 1
    print(f"[{count: >8} files]")
    return mapped


def main():
    cwd = Path.cwd().resolve()
    args = argparser.parse_args(namespace=Args())

    mapped = gather(cwd, args)
    conflicts = {k: v for k, v in mapped.items() if len(v) > 1}

    if conflicts:
        # lol pprint
        print("{")
        for k, v in conflicts.items():
            print(f"    \"{k}\": [")
            for i in v:
                print(f"        r\"{i.relative_to(cwd)}\",")
            print("    ],")
        print("}")
    else:
        print("{}")

    return 0


if __name__ == '__main__':
    try:
        exit(main())
    except Exception as e:
        exit(f"{e.__class__.__name__}: {e}")
