import os
from typing import List


class Dir:

    def __init__(self, path: str) -> None:
        self.path = path
        self.dirs: List["Dir"] = []
        self.files: List[str] = []

        for r, d, f in os.walk(self.path):
            self.dirs.extend([Dir(os.path.join(r, i)) for i in d])
            self.files.extend(f)
            break  # not a deep walk
        self.__count = None

    @property
    def count(self) -> int:
        if self.__count is not None:
            return self.__count

        count = 0

        count += len(self.files)
        for i in self.dirs:
            count += i.count

        self.__count = count
        return count


def render(o: Dir, level: int = 0):
    print(f"{'    '*level}[{o.count: >6}] {os.path.split(o.path)[1]}")
    for i in o.dirs:
        render(i, level+1)


def main():
    root = Dir(os.getcwd())

    render(root)


if __name__ == "__main__":
    main()
