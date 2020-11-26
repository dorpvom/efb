import logging
import sys
from copy import deepcopy
from pathlib import Path
from typing import List

from efb.discovery import FileDiscoverer
from efb.terminal import SESSION, make_decision, print_
from efb.validator import RangeValidator


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
    ask_for_each_file = make_decision('Decide action for each file (or always keep first duplicate)?', default=True)
    for _, files in fd.hashes.items():
        if len(files) > 1:
            delete_duplicates(files, ask_for_each_file=ask_for_each_file)


def get_paths_as_strings(files: List[Path]) -> List[str]:
    return [str(file_) for file_ in _omit_common_root(files)]


def _omit_common_root(files: List[Path]) -> List[Path]:
    if not files:
        return files

    ref, common = files[0], None

    for parent in ref.parents:
        if all(str(file).startswith(str(parent)) for file in files):
            common = parent
            break

    if not common:
        return files

    return [file_.relative_to(common) for file_ in files]


def delete_duplicates(files: List[Path], ask_for_each_file: bool) -> None:
    print_(f'Found {files[0]} with {len(files) - 1} duplicates:')
    print_(get_paths_as_strings(files))
    if ask_for_each_file:
        input_range = list(range(len(files)))
        options = ', '.join((str(index) for index in input_range))
        to_keep = SESSION.prompt(
            f'Which file do you want to keep? {options} (Empty: Keep all): ',
            validator=RangeValidator(input_range=input_range)
        )
        try:
            if to_keep:
                keeping = files.pop(int(to_keep))
            else:
                keeping = deepcopy(files)
                files = []
        except ValueError:
            print_('[Error] Bad index. Either you did not given an integer or it was out of range')
            return
    else:
        keeping = files.pop(0)

    print_(f'Keeping {keeping}\nDeleting {get_paths_as_strings(files)}')
    for file_ in files:
        file_.unlink()


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
