import sys
from typing import List
from pathlib import Path


class Options:
    folders: List[Path]
    cwd: Path
    deep: bool

    def __init__(self):
        self.cwd = Path.cwd().resolve()
        self.folders = []
        self.deep = False

        args = sys.argv[1:]
        for arg in args:
            if arg == "--deep":
                self.deep = True
                continue
            path = Path(arg)
            if path.exists() and path.is_dir():
                self.folders.append(path)
        if not self.folders:
            for x in self.cwd.iterdir():
                if x.is_dir():
                    self.folders.append(x)


def empty(directory: Path) -> bool:
    """
        Is directory empty?
    """
    return next(directory.iterdir(), None) is None


def clamp(directory: Path) -> bool:
    """
        Try to rm directory
    """
    try:
        directory.rmdir()
        print(f"clamp \"{directory}\";")
        return True
    except Exception:
        return False


def main() -> int:
    options = Options()

    stack = options.folders.copy()

    while stack:
        folder = stack.pop(0)

        if empty(folder):
            clamp(folder)
            continue

        if not options.deep:
            continue

        for some in folder.iterdir():
            if some.is_dir():
                if empty(some):
                    clamp(some)
                    if folder not in stack:
                        stack.append(folder)
                else:
                    stack.append(some)
    return 0


if __name__ == "__main__":
    exit(main())
