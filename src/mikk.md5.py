import hashlib
import sys
from pathlib import Path


CHUNK_SIZE = 4194304  # 4 MB


def calc_hash(file: Path) -> str:
    md5 = hashlib.md5()
    with file.open("rb") as fp:
        while True:
            chunk = fp.read(CHUNK_SIZE)
            if not chunk:
                break
            md5.update(chunk)
    return md5.hexdigest()


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
        md5 = calc_hash(path)
        print(F"{md5} \"{path}\"")
    return 0


if __name__ == '__main__':
    exit(main())