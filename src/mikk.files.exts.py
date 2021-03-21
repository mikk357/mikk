from pathlib import Path


def main():
    cwd = Path.cwd()

    exts = {some.suffix for some in cwd.glob("*.*") if some.is_file()}

    print(*exts)

    return 0


if __name__ == '__main__':
    exit(main())
