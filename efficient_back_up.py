import logging
import sys
from copy import deepcopy
from pathlib import Path
from typing import List

from efb.discovery import FileDiscoverer
from efb.terminal import SESSION, print_


def identify_files_to_backup():
    fd = FileDiscoverer()
    fd.discover_files()

    print_('\n Now to our backup volume')

    # Find backup volumes
    bd = FileDiscoverer()
    bd.discover_files()

    # For each file check if backup volumes contain file
    existing, not_existing = 0, 0
    for hash_, files in fd.hashes.items():
        if hash_ in bd.hashes:
            logging.debug(f'Found existing file {files} on backup')
            existing += len(files)
        else:
            logging.info(f'{files} need to be backed up')
            not_existing += len(files)

    print_(f'Found {existing} files present on backup drive and {not_existing} to back up.')
    # Store everything and make it listable


def identify_duplicates():
    fd = FileDiscoverer()
    fd.discover_files()
    for _, files in fd.hashes.items():
        if len(files) > 1:
            delete_duplicates(files)
    # Option 1: Keep first element always. Option 2: Decide for each file.


def get_names(files: List[Path]) -> List[str]:
    return [str(file_) for file_ in files]


def delete_duplicates(files: List[Path]) -> None:
    # FIXME Show paths relative
    print_(f'Found {files[0]} with {len(files) - 1} duplicates:')
    print_(get_names(files))
    options = ', '.join((str(index) for index, _ in enumerate(files)))
    to_keep = SESSION.prompt(f'Which file do you want to keep? Options: {options} (Empty: Keep all)')
    try:
        if to_keep:
            to_keep = int(to_keep)
            if to_keep < 0 or to_keep >= len(files):
                raise ValueError('Index out of range')
            keeping = files.pop(to_keep)
        else:
            keeping = deepcopy(files)
            files = []
    except ValueError:
        print_('[Error] Bad index. Either you did not given an integer or it was out of range')
        return
    print_(f'Keeping {keeping}\nDeleting {get_names(files)}')
    for file_ in files:
        file_.unlink(missing_ok=True)


def main():  # pylint: disable=too-complex
    '''
    Options:
    - Identify files to back up: List of files to back up
    - Find duplicates
    '''
    choice = SESSION.prompt(
        'What do you want to do?\n'
        '- Find duplicate files [d]\n'
        '- Identify files that need to be backed up [i]\n'
        '- Back up files [b]\n'
        '\n'
        'Please state your choice [d/i/b]: '
    )

    if choice == 'i':
        try:
            identify_files_to_backup()
        except KeyboardInterrupt:
            print_('Aborting ...')
            return 255

    elif choice == 'd':
        try:
            identify_duplicates()
        except KeyboardInterrupt:
            print_('Aborting ...')
            return 255

    elif choice == 'b':
        print_('Not implemented yet.')

    else:
        print_(f'Invalid choice {choice}. Aborting.')
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
