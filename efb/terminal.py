from typing import Optional

from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as print_

from efb.validator import YesNoValidator

SESSION = PromptSession()


def make_decision(question: str, default: Optional[bool] = None) -> bool:
    default_string = f'(default {"y" if default else "n"})' if default is not None else ''

    while True:
        answer = SESSION.prompt(f'{question} [y/n] {default_string}: ', validator=YesNoValidator())
        if answer == 'y':
            return True
        if answer == 'n':
            return False
        if not answer and default is not None:
            return default
        print_(f'Please state your decision as y or n (not {answer}')
