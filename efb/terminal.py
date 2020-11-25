from typing import Callable, Optional

from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as print_

from efb.validator import YesNoValidator

SESSION = PromptSession()


def make_decision(question: str, default: Optional[str] = None, rprompt: Optional[Callable] = None) -> bool:
    default_string = f'[y/n] (default {default})'

    while True:
        answer = SESSION.prompt(f'{question} {default_string}', rprompt=rprompt, validator=YesNoValidator())
        if answer in ['y', 'Y'] or (not answer and default in ['y', 'Y']):
            return True
        if answer in ['n', 'N'] or (not answer and default in ['n', 'N']):
            return False
        print_(f'Please state your decision as y or n (not {answer}')
