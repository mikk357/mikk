import time
import sys


nums = set("0123456789")


def bell():
    print(chr(7), end="", flush=True)


def main():
    args = sys.argv[1:]
    if not args:
        return "err: no arguments passed"

    span = 0
    number = 1

    _args = args.copy()
    if _args[0] == "a":
        _args.pop(0)
    while _args:
        arg = _args.pop(0).lower()
        # isdigit is dumb
        if set(arg).issubset(nums):
            number = int(arg)
        elif arg in ("s", "sec", "second", "seconds"):
            span += number * 1
            number = 1
        elif arg in ("m", "min", "minute", "minutes"):
            span += number * 60
            number = 1
        elif arg in ("h", "hour", "hours"):
            span += number * 3600
            number = 1
        else:
            return f"err: unknown expression: {arg}"

    if span:
        print(f"waiting for {span} seconds...")
        time.sleep(span)
        for _ in range(3):
            bell()
    else:
        return "err: 0 seconds"


if __name__ == '__main__':
    exit(main())
