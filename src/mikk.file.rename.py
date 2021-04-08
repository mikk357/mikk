
from typing import List, Dict, Union
from pathlib import Path
import hashlib
from argparse import ArgumentParser


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


def filehash(file: Path, mode: str = "sha256") -> str:
    """
        returns file hash as hex string
    """
    if mode == "sha256":
        _hash = hashlib.sha256()
    elif mode == "md5":
        _hash = hashlib.md5()
    else:
        raise Exception(f"unknown hash {mode}")

    with file.open("rb") as fh:
        while True:
            chunk = fh.read(CHINK_SIZE)
            if not chunk:
                break
            _hash.update(chunk)
    return _hash.hexdigest()


def main() -> Union[int, str]:
    args = argparser.parse_args()
    code = 0

    if args.files:
        files: List[Path] = []
        for arg in args.files:
            if arg == "*":
                files.extend(i for i in Path.cwd().iterdir() if i.is_file())
                continue
            path = Path(arg)
            if not path.exists():
                raise Exception(f"file \"{path}\" not exists")
            elif not path.is_file():
                raise Exception(f"object \"{path}\" not a file")
            else:
                files.append(path)

        for file in files:
            try:
                if args.mode == "sha256":
                    name_ = filehash(file)
                elif args.mode == "md5":
                    name_ = filehash(file, mode="md5")
                elif args.mode == "ts":
                    raise NotImplementedError()
                else:
                    raise Exception("invalid renaming mode")

                new_name = file.parent / (name_ + "".join(file.suffix))
                if new_name == file:
                    continue  # renaming doesn't required
                if new_name.exists():
                    raise Exception(f"file \"{new_name}\" already exists")
                print(f"\"{file}\" -> \"{new_name}\"")
                file.rename(new_name)
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
