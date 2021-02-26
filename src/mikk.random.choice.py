import sys
import os
import stat
import random


def is_piped() -> bool:
    """ echo something | __file__ ? """
    if stat.S_ISFIFO(os.fstat(0).st_mode):
        return True
    else:
        return False


def main():
    args = sys.argv[1:]
    variants = []

    if is_piped():
        for line in sys.stdin:
            variants.append(line.rstrip())
    else:
        variants.extend(args)

    if variants:
        selected = random.choice(variants)
        print(selected)
    else:
        print("ERR: no variants")


if __name__ == '__main__':
    main()
