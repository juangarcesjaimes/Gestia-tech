# (12) validators.py - Validadores personalizados (para emails, contraseñas, etc.)

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_email(value):
    """
    Valida que el email tenga un formato correcto.
    
    Args:
        value (str): El email a validar.
        
    Raises:
        ValidationError: Si el formato del email es incorrecto.
    """
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
        raise ValidationError(_('Formato de email no válido.'), code='invalid_email')

def validate_password(value):
    """
    Valida que la contraseña cumpla con ciertos requisitos de seguridad.
    
    La contraseña debe tener al menos 8 caracteres, al menos una letra mayúscula,
    una letra minúscula y un número.

    Args:
        value (str): La contraseña a validar.
        
    Raises:
        ValidationError: Si la contraseña no cumple con los requisitos.
    """
    if len(value) < 8:
        raise ValidationError(_('La contraseña debe tener al menos 8 caracteres.'), code='password_too_short')
    
    if not re.search(r'[A-Z]', value):
        raise ValidationError(_('La contraseña debe contener al menos una letra mayúscula.'), code='no_uppercase_letter')
    
    if not re.search(r'[a-z]', value):
        raise ValidationError(_('La contraseña debe contener al menos una letra minúscula.'), code='no_lowercase_letter')
    
    if not re.search(r'[0-9]', value):
        raise ValidationError(_('La contraseña debe contener al menos un número.'), code='no_number')

def validate_username(value):
    """
    Valida que el nombre de usuario contenga solo caracteres permitidos.
    
    Args:
        value (str): El nombre de usuario a validar.
        
    Raises:
        ValidationError: Si el nombre de usuario contiene caracteres no permitidos.
    """
    if not re.match(r'^[\w.@+-]+$', value):
        raise ValidationError(_('El nombre de usuario contiene caracteres no permitidos.'), code='invalid_username')
