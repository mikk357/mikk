
COUNT = 2


def bell():
    print(chr(7), end="\r")


def main():
    for i in range(COUNT):
        bell()


if __name__ == '__main__':
    main()
