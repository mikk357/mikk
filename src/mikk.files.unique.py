from argparse import ArgumentParser
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


CHINK_SIZE = 8388608  # 8MB


def filehash(file: Path) -> str:
    _hash = hashlib.sha256()
    with file.open("rb") as fh:
        while True:
            chunk = fh.read(CHINK_SIZE)
            if not chunk:
                break
            _hash.update(chunk)
    return _hash.hexdigest()


def gather(cwd: Path, deep: bool = False) -> Dict[str, List[Path]]:
    mapped: Dict[str, List[Path]] = dict()
    glob_ = (cwd.rglob("*") if deep else cwd.glob("*"))
    gen = (i for i in glob_ if i.is_file())
    count = 0

    for file in gen:
        print(f"[{count: >8} files]", end="\r")
        hash_hex = filehash(file)
        if hash_hex in mapped:
            mapped[hash_hex].append(file)
        else:
            mapped[hash_hex] = [file]
        count += 1
    print(f"[{count: >8} files]")
    return mapped


def main():
    cwd = Path.cwd().resolve()
    args = argparser.parse_args()

    mapped = gather(cwd, args.deep)
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
