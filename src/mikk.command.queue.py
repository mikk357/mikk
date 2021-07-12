import os
import sys


__doc__ = """\
command `mikk.command.queue tasks.bat` will
    - read shell commands from file
    - for each non-empty line do
        - execute line
        - if there are more lines, prompt for continuation
\
"""


def main():
    args = sys.argv[1:]

    if (
        not args
        or args == ["-h"]
        or args == ["--help"]
    ):
        print(__doc__)
        exit(1)

    files = []

    for arg in args:
        if os.path.exists(arg) and os.path.isfile(arg):
            files.append(arg)
        else:
            raise FileNotFoundError(f"file \"{arg}\" not exists!")

    for file in files:

        lines = []
        with open(file, "r", encoding="utf8") as fp:
            lines = [line.rstrip() for line in fp]

        while lines:
            line = lines.pop(0)
            if not line.startswith(("::", "//", "#")):
                print(f"execute {line}")
            else:
                print(line.rstrip())
            if lines:
                input()


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("execution interrupted from keyboard;")
        exit(0)
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}")
