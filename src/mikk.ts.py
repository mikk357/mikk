import sys
import datetime


translation = str.maketrans({"T": "_", ":": "-"})

nums = set("0123456789")


def main():

    now = datetime.datetime.now()

    formats = {
        "now": now.strftime("%H:%M:%S, %A %d, %B %Y"),
        "iso": now.isoformat(),
        "safe": now.isoformat().translate(translation),
    }

    args = sys.argv[1:]
    if args:
        if set(args[0]).issubset(nums):
            index = int(args[0])
            values = tuple(formats.values())
            print(values[index])
        elif args[0] in formats:
            print(formats[args[0]])
    else:
        for k, v in formats.items():
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
