import os
import sys
from typing import List, Dict
from pathlib import Path


__doc__ = """
--list                 print all executable files which in PATH
--conflicts            find possible conflicts
--find <str>           search executables with `str` in file name
"""


def main():
    path = os.environ.get("PATH")
    if path is None:
        print("ERROR: no environment variable PATH")
        return 1
    path = sorted(
        Path(i) for i in path.split(os.pathsep)
        if (i != "")
    )
    # print("path: [\n\t" + "\n\t".join(map(str, path)) + "\n]")

    pathext = os.environ.get("PATHEXT")
    if pathext is None:
        print("ERROR: no environment variable PATHEXT")
        return 1
    pathext = {
        i.lower() for i in pathext.split(os.pathsep)
        if (i != "")
    }
    # print(f"pathext: {pathext}")

    args = sys.argv[1:]
    # print(f"args: {args}")

    files = [
        j
        for i in path
        for j in i.glob("*.*")
        if j.suffix in pathext
    ]

    if "--list" in args:
        names = sorted(map(str, files))
        print(*names, sep="\n")

    elif "--conflicts" in args:
        mapped: Dict[str, List[Path]] = {}
        for file in files:
            if file.name in mapped:
                mapped[file.name].append(file)
            else:
                mapped[file.name] = [file]
        for _name, _files in mapped.items():
            if len(_files) > 1:
                print(f"[{_name}]")
                for _file in _files:
                    print(f" -- {_file}")

    elif "--find" in args and args[1:]:
        target = sys.argv[2]
        for file in files:
            if target in file.name:
                print(f"{file.parent} :: {file.name}")

    else:
        print(__doc__)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        __import__("traceback").print_tb()
