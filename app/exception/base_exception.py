"""
    BASE EXCEPTION FILE
"""
from fastapi import HTTPException, status

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User Does Not Exist! Please Register First.",
)

user_found = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with this email already Exist!",
)

invalid_email = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid Email!",
)

invalid_password = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid Password!",
)

invalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Credentials!",
)

category_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Category Does Not Exist!",
)

tag_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Tag Does Not Exist!",
)

post_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Post Does Not Exist!",
)
