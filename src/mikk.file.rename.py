from argparse import ArgumentParser
from hashlib import md5, sha256
from pathlib import Path
from typing import List, Union
from datetime import datetime


argparser = ArgumentParser()
argparser.add_argument(
    "--mode",
    help="renaming logic mode",
    dest="mode",
    default="sha256",
    required=False,
)
argparser.add_argument(
    "files",
    metavar="F",
    help="files to rename",
    nargs="+",
    type=str,
)

CHINK_SIZE = 8388608  # 8MB


def filehash(file: Path, mode=sha256) -> str:
    """
        returns file hash as hex string
    """

    _hash = mode()
    with file.open("rb") as fh:
        while True:
            chunk = fh.read(CHINK_SIZE)
            if not chunk:
                break
            _hash.update(chunk)
    return _hash.hexdigest()


def files_from_args(arr: List[str]) -> List[Path]:
    out: List[Path] = []
    for i in arr:
        if "*" in i:
            out.extend(i for i in Path.cwd().glob(i) if i.is_file())
            continue
        path = Path(i)
        if not path.exists():
            raise Exception(f"file \"{path}\" not exists")
        elif not path.is_file():
            raise Exception(f"object \"{path}\" not a file")
        else:
            out.append(path.absolute())
    return out


def main() -> Union[int, str]:
    args = argparser.parse_args()
    code = 0
    cwd = Path.cwd().resolve()

    if args.files:
        files = files_from_args(args.files)

        for file in files:
            try:
                if args.mode == "sha256":
                    name_ = filehash(file)
                elif args.mode == "md5":
                    name_ = filehash(file, mode=md5)
                elif args.mode == "mtime":
                    name_ = datetime\
                        .fromtimestamp(file.stat().st_mtime)\
                        .strftime("%Y-%m-%d_%H-%M-%S")
                else:
                    raise Exception("invalid renaming mode")

                file_new = file.parent / (name_ + file.suffix)
                if file_new == file:
                    continue  # renaming doesn't required
                print(f"\"{file.relative_to(cwd)}\" -> \"{file_new.relative_to(cwd)}\"")
                if file_new.exists():
                    print("error: file already exists")
                    continue
                file.rename(file_new)
            except Exception as e:
                print(
                    "Error during renaming:\n\t"
                    f"{e.__class__.__name__}: {e}"
                )
                code += 1  # increment exit code
        return code

    else:
        return "Error: no files passed"


if __name__ == '__main__':
    exit(main())
