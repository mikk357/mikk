from pathlib import Path


def separate(path: Path):
    files = []
    dirs = []

    for i in path.iterdir():
        if i.is_file():
            files.append(i)
            continue
        if i.is_dir():
            dirs.append(i)
            continue

    return (dirs, files)


def main():
    cwd = Path.cwd().resolve()
    stack = [cwd]
    count = 0

    while stack:
        path = stack.pop(0)
        data = separate(path)
        stack.extend(data[0])
        count += len(data[1])

    print(f"\t{count} files")


if __name__ == '__main__':
    main()
