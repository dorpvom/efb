from prompt_toolkit.validation import Validator, ValidationError


class YesNoValidator(Validator):
    def validate(self, document):
        if document.text and document.text not in ['y', 'n']:
            raise ValidationError(message=f'Your input has to either be *y* or *n*. Got {document.text}')


class NumberValidator(Validator):
    def validate(self, document):
        if document.text and not document.text.isdigit():
            raise ValidationError(message=f'Your input has to be a number. Got {document.text}')


class RangeValidator(NumberValidator):
    def __init__(self, *args, **kwargs):
        super(Validator).__init__(*args, **kwargs)
        self.input_range = kwargs['input_range']

    def validate(self, document):
        super(NumberValidator).validate(document)
        if not int(document.text) in self.input_range:
            raise ValidationError(message=f'Your input is out of range {self.input_range}. Got {document.text}.')