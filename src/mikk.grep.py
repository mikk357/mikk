import sys
import re


__doc__ = f"""
not a real grep, just regex.search(line) for line in input stream

dir /s /b | {__file__} .+\\.(exe^|bat)
(windows cmd)
"""


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1

    try:
        regex = re.compile(args[0])
    except Exception as e:
        return f"err: exception during regex compilation: {e}"

    for line in sys.stdin:
        line = line.rstrip()
        if regex.search(line):
            print(line)


if __name__ == '__main__':
    exit(main())
