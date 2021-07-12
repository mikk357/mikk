COUNT = 2


def bell():
    print(chr(7), end="", flush=True)


def main():
    for _ in range(COUNT):
        bell()
    print()


if __name__ == '__main__':
    main()
