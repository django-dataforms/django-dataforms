from django.core.exceptions import ValidationError


# Bindings use '___' as the value delimiter for choices.
def reserved_delimiter(value):
    if '___' in value:
        raise ValidationError("This cannot contain a '___' because it is a reserved delimiter.")