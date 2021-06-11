from typing import Dict, List
from pathlib import Path


class Main:
    def __init__(self):
        self.cwd = Path.cwd().resolve()

    def gather(self, mkdir: bool = True) -> Dict[Path, List[Path]]:
        mapped: Dict[str, List[Path]] = {
            "other": []
        }

        for i in self.cwd.rglob("*"):
            if not i.is_file():
                continue  # skip non-file
            if i.suffix:
                if i.suffix in mapped:
                    mapped[i.suffix].append(i)
                else:
                    mapped[i.suffix] = [i]
            else:
                mapped["other"].append(i)

        out = {(self.cwd / ext): files for ext, files in mapped.items()}

        if mkdir:
            for folder in out.keys():
                if not folder.exists():
                    folder.mkdir()

        return out

    @staticmethod
    def move(old: Path, new: Path):
        if new == old:
            return
        if new.exists():
            print(
                f"can't move \"{old}\"\n"
                f"   because \"{new}\"\n"
                "already exists;"
            )
            return
        if new != old and not new.exists():
            try:
                old.replace(new)
            except Exception as e:
                print(f"\"{old}\" => \"{new}\":")
                print(e)
                print()

    def main(self):
        mapped = self.gather()
        for folder, files in mapped.items():
            for file in files:
                new = folder / file.name
                self.move(file, new)


if __name__ == "__main__":
    try:
        Main().main()
    except Exception as e:
        print(f"{e.__class__}: {e}")
