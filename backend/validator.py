from django.core.validators import RegexValidator

validate_phone = RegexValidator(
    regex=r"^\+?1?\d{8,8}$",
    message="El número de teléfono debe estar en el formato: '88888888'. "
    "8 dígitos permitidos.",
)
