import time
import sys


nums = set("0123456789")


def bell():
    print(chr(7), end="", flush=True)


def main():
    args = sys.argv[1:]
    if not args:
        return "err: no arguments passed"

    start = time.time()
    timespan = 0
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
            timespan += number * 1
            number = 1
        elif arg in ("m", "min", "minute", "minutes"):
            timespan += number * 60
            number = 1
        elif arg in ("h", "hour", "hours"):
            timespan += number * 3600
            number = 1
        else:
            return f"err: unknown expression: {arg}"

    if timespan:

        end = start + timespan
        while time.time() < end:
            diff = end - time.time()
            h = int(diff // 3600)
            m = int(diff % 3600 // 60)
            s = int(diff % 3600 % 60)
            print(f"{h:0>2}:{m:0>2}:{s:0>2}", end="\r")
            time.sleep(0.5)
        print("\n")
        for _ in range(3):
            bell()

    else:
        return "err: 0 seconds"


if __name__ == '__main__':
    exit(main())
