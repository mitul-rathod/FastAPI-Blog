"""
    UTILITY FILE
"""

from datetime import datetime, timedelta
from typing import Optional, Union, List

from email_validator import validate_email
from password_validator import PasswordValidator
from jose import jwt

from app.exception.base_exception import invalid_email
from app import schemas
from app.core.configuration import settings


def is_email_valid(email):
    """
    Validate Email
    """
    try:
        if user_email := validate_email(email=email):
            return user_email.email.lower()
    except Exception as e:
        raise invalid_email from e


def is_valid_password(password):
    """
    Validate Password
    """
    schema = PasswordValidator()
    schema.min(10).max(
        20
    ).has().letters().has().uppercase().has().lowercase().has().digits().has().symbols().has().no().spaces()
    return schema.validate(password)
