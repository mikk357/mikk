
from typing import List, Dict
from pathlib import Path
import hashlib


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


def gather(cwd: Path) -> Dict[str, List[Path]]:
    """  """
    mapped = {}
    gen = (i for i in cwd.glob("*.*") if i.is_file())
    count = 0

    for file in gen:
        print(f"[{count: >8} files]", end="\r")
        _hash = filehash(file)
        if _hash in mapped:
            mapped[_hash].append(file)
        else:
            mapped[_hash] = [file]
        count += 1
    print(f"[{count: >8} files]")
    return mapped


def main():
    cwd = Path.cwd().resolve()
    rel = lambda x, r = str(cwd): str(file).replace(r, ".", 1)

    mapped = gather(cwd)

    for hash_, files in mapped.items():
        if len(files) > 1:
            print(f"hash: [{hash_}]")
            for file in files:
                print(f"    {rel(file)}")

    return 0


if __name__ == '__main__':
    exit(main())
