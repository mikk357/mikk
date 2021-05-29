import sys


def main():
	lines = set()
	for line in sys.stdin:
		lines.add(line)

	for line in lines:
		sys.stdout.write(line)

	return 0


if __name__ == "__main__":
	exit(main())