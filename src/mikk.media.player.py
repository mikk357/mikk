import code
import os
import random
import time
from pathlib import Path
from typing import Union

import click


exts = {
    f"{os.extsep}{i}"
    for i in ("m4a", "mp3", "opus", "mp4", "webm", "flac")
}


class Track:
    name: str
    path: Path

    def __init__(self, path: Union[Path, str]):
        if isinstance(path, str):
            self.path = Path(path)
        else:
            self.path = path
        self.name = self.path.name

    def __repr__(self):
        return f"<Track \"{self.path.name}\">"


class Playlist(list):
    def __init__(self) -> None:
        super().__init__()
        self.__i = 0

    def gather(self, loc: Union[Path, str], deep: bool = True) -> None:
        for p, d, f in os.walk(loc):
            self.extend(
                Track(i) for i in (Path(p, i).resolve() for i in f)
                if i.is_file() and i.suffix in exts
            )
            if not deep:
                break

    @property
    def current(self) -> Track:
        if 0 <= self.__i < self.__len__():
            return self[self.__i]
        else:
            raise IndexError(f"playlist[{self.__i}] is out of bounds")

    @property
    def prev(self) -> Track:
        if self.__i - 1 >= 0:
            self.__i -= 1
        else:
            self.__i = self.__len__() - 1
        return self[self.__i]

    @property
    def next(self) -> Track:
        if self.__i + 1 < self.__len__():
            self.__i += 1
        else:
            self.__i = 0
        return self[self.__i]

    def drop(self):
        try:
            self.pop(self.__i)
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")


def play(track: Track, slow: bool = True):
    print(f"playing {track.name}")
    _cmd = (
        f"vlc --started-from-file \"{track.path}\""
    )
    if slow:
        time.sleep(0.2)
    os.system(_cmd)


def enqueue(track: Track, slow: bool = True):
    print(f"enqueue {track.name}")
    _cmd = (
        f"vlc --started-from-file --playlist-enqueue \"{track.path}\""
    )
    if slow:
        time.sleep(0.2)
    os.system(_cmd)


@click.command()
@click.option("--auto", is_flag=True, default=False)
def main(auto: bool):
    playlist = Playlist()
    cwd = Path.cwd()

    def autostart(count: int = 64):
        playlist.gather(cwd)
        random.shuffle(playlist)
        play(playlist.current)
        for _ in range(count):
            enqueue(playlist.next)

    if auto:
        autostart()
        return

    local = dict(
        cwd=cwd,
        playlist=playlist,
        pl=playlist,
        play=play,
        auto=auto,
        enqueue=enqueue,
        random=random,
        choice=random.choice,
        shuffle=random.shuffle
    )

    code.interact(local=local, banner="", exitmsg="")


if __name__ == '__main__':
    main()
