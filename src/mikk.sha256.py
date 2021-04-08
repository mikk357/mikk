import hashlib
import sys
from pathlib import Path


CHUNK_SIZE = 4194304  # 4 MB


def filehash(file: Path) -> str:
    _hash = hashlib.sha256()
    with file.open("rb") as fp:
        while True:
            chunk = fp.read(CHUNK_SIZE)
            if not chunk:
                break
            _hash.update(chunk)
    return _hash.hexdigest()


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print("ERR! no args")
        return 1
    for i in args:
        path = Path(i)
        if not path.exists():
            print(F"ERR! \"{path}\" not exists")
            return 1
        if not path.is_file():
            print(F"ERR! \"{path}\" not a file")
            return 1
        _hash = filehash(path)
        print(F"{_hash} \"{path}\"")
    return 0


if __name__ == '__main__':
    exit(main())
