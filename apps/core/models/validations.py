from django.core.exceptions import ValidationError

def validate_max_value(value) -> None:
   if value > 100:
       raise ValidationError(
           "%(value)s es mayor que el valor máximo permitido (100)",
           params={"value": value},
       )
       
def validate_letters(value):
    if not value.isalpha():
        raise ValidationError(
            'Este campo solo puede contener letras',
            code='invalid_letters'
        )