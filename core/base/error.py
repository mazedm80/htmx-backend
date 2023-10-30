from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    def __init__(
        self, detail: str = "Unauthorized", headers={"WWW-Authenticate": "Bearer"}
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers
        )


# validation exception class
class ValidationException(HTTPException):
    def __init__(
        self, detail: str = "Validation Error", headers={"WWW-Authenticate": "Bearer"}
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            headers=headers,
        )


# database insert exception class
class DatabaseInsertException(HTTPException):
    def __init__(
        self,
        detail: str = "Error while inserting data",
        headers={"WWW-Authenticate": "Bearer"},
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=headers,
        )


# database query exception class
class DatabaseQueryException(HTTPException):
    def __init__(
        self,
        detail: str = "Error while executing query",
        headers={"WWW-Authenticate": "Bearer"},
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=headers,
        )


# email exists exception class
class EmailExistsException(HTTPException):
    def __init__(
        self,
        detail: str = "Email already exists",
        headers={"WWW-Authenticate": "Bearer"},
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=headers,
        )
