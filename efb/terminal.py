from typing import Optional, Callable
from prompt_toolkit import PromptSession

SESSION = PromptSession()


def make_decision(question: str, default: Optional[str] = None, rprompt: Optional[Callable] = None) -> bool:
    default_string = f'[y/n] (default {default})'

    while True:
        answer = SESSION.prompt(f'{question} {default_string}', rprompt=rprompt)
        if answer in ['y', 'Y'] or (not answer and default in ['y', 'Y']):
            return True
        if answer in ['n', 'N'] or (not answer and default in ['n', 'N']):
            return False
        print(f'Please state your decision as y or n (not {answer}')