# Efficient Back Up
-- efficient as in less duplicates

## Idea

I started to dread my ever growing back up drives since I seem to mostly just back up all my data blindly instead of
sorting them in any concise way. This resulted in a drive with root folders such as PC1, PC2, PC2.newer, ...
Ever been there?

EFB will one day hopefully help to sort out this mess. Some things I want to build before I'm done:

- Check which files are already backed up to avoid unnecessary transfer.
- Find existing duplicates on back up drives.
- Offer interface to back up data nicely.
- ...

Limitations:

- **Does not work yet**
- Excludes dot folders as of now
- Ignores files > 1 GB due to computational complexity of hash (but logs, the ignore)
- ...

## Tech

Based on [Python Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) for the CLI, pathlib for discovery and SHA256 as checksum to identify files.

## Contribute?

Shure, any help is welcome. Leave an Issue or open a pull request anytime.
