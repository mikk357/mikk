import random
from pathlib import Path


def main():
    cwd = Path.cwd().resolve()

    files = [i for i in cwd.glob("*.*") if i.is_file()]

    file = random.choice(files)

    print(f"\"{file.name}\"")


if __name__ == '__main__':
    main()
