import logging

from efb.discovery import FileDiscoverer
from efb.terminal import SESSION


def identify_files_to_backup():
    fd = FileDiscoverer()
    fd.discover_files()

    print('\n Now to our backup volume')

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

    print(f'Found {existing} files present on backup drive and {not_existing} to back up.')
    # Store everything and make it listable


def identify_duplicates():
    fd = FileDiscoverer()
    fd.discover_files()
    for hash_, files in fd.hashes.items():
        if len(files) > 1:
            print(files)


def main():
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
            print('Aborting ...')
            return 255

    elif choice == 'd':
        try:
            identify_duplicates()
        except KeyboardInterrupt:
            print('Aborting ...')
            return 255

    elif choice == 'b':
        print('Not implemented yet.')

    else:
        print(f'Invalid choice {choice}. Aborting.')
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
