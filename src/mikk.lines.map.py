import os
import random
import re
import sys
from pathlib import Path


namespace = {}
namespace.update(locals())
namespace.update(globals())


def main():
    args = sys.argv[1:]

    stdin = sys.stdin
    stdout = sys.stdout

    if args:
        try:
            code = compile(args[0], "<string>", "eval")
        except Exception as e:
            print("error during compiling expression")
            print(f"{e.__class__.__name__}: {e}")
            exit(1)

        for line in stdin:
            stdout.write(
                eval(code, namespace, {"line": line[:-1]})
            )
            stdout.write("\n")

    else:
        print("provide python expression")
        exit(2)


if __name__ == "__main__":
    exit(main())
