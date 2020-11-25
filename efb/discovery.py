import logging
from hashlib import sha256
from pathlib import Path
from typing import Iterable

from common_helper_process import execute_shell_command
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.shortcuts import ProgressBar

from efb.terminal import make_decision, SESSION

HASH_SOFT_CAP = 100 * 1000 * 1000
HASH_HARD_CAP = 1000 * 1000 * 1000
INCLUDE_DOT_FILES = True
INCLUDE_DOT_FOLDERS = False


class FileDiscoverer:
    def __init__(self):
        self.fs_roots = []
        self.files = []
        self.hashes = {}
        self.unsupported_files = []

    def discover_files(self):
        self.select_fs_roots()
        self.iterate_fs_roots()
        self.compute_hashes()
        self.exclude_root_files()

    def exclude_root_files(self):
        for file_ in self.unsupported_files:
            print(f'Found unsupported file {file_}')
            self.files.remove(file_)

    def iterate_fs_roots(self):
        for root in self.fs_roots:
            self._iterate_dir(Path(root))
            print(f'Found {len(self.files)} files on {root}.')

    def _iterate_dir(self, directory: Path):
        self.files.extend(iterate_root(directory))

    def compute_hashes(self):
        with ProgressBar() as bar:
            for file_ in bar(self.files, total=len(self.files)):
                try:
                    if file_.stat().st_size > HASH_HARD_CAP:
                        print(f'Not hashing {file_} due to size limit. Please back up by hand if wanted.')
                        continue
                    elif file_.stat().st_size > HASH_SOFT_CAP:
                        hash_ = execute_shell_command(f'sha256sum "{file_.absolute()}"', timeout=30).split()[0]
                    else:
                        hash_ = sha256(file_.read_bytes()).hexdigest()
                    self.hashes.setdefault(hash_, []).append(file_)
                except (PermissionError, FileNotFoundError, IndexError):
                    self.unsupported_files.append(file_)

    def select_fs_roots(self):
        while make_decision('Do you wish to add a root?', default='y', rprompt=lambda: str(self.fs_roots)):
            self.add_root()

    def add_root(self):
        answer = SESSION.prompt('Please state your new root as path: ', completer=PathCompleter(), rprompt=lambda: str(self.fs_roots))
        if not Path(answer).exists():
            print(f'{answer} is no path on this system')
        elif not Path(answer).is_dir():
            print(f'Roots must be directories. {answer} is not.')
        else:
            self.fs_roots.append(answer)


def iterate_root(path: Path) -> Iterable[Path]:
    if not path.is_symlink() and path.is_dir():
        for child_path in path.iterdir():
            yield from _iterate_path_recursively(child_path, )
    else:
        yield from []


def _iterate_path_recursively(path: Path):
    try:
        if path.is_symlink():
            pass
        elif path.is_file():
            if INCLUDE_DOT_FILES or not path.name.startswith('.'):
                yield path
        elif path.is_dir():
            if INCLUDE_DOT_FOLDERS or not path.name.startswith('.') or path.name.startswith('...'):
                for child_path in path.iterdir():
                    yield from _iterate_path_recursively(child_path)
    except PermissionError:
        logging.error(f'Permission Error: could not access path {path.absolute()}')
    except OSError:
        logging.warning(f'possible broken symlink: {path.absolute()}')
    yield from []
