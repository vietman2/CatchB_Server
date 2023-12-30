from django.core import validators
from django.utils.deconstruct import deconstructible

@deconstructible
class CustomUsernameValidator(validators.RegexValidator):
    regex = r'^[\w]+\Z'
    message = 'Enter a valid username. This value may contain only letters and numbers.'
    flags = 0
