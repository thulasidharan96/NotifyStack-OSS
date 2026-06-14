from fastapi import HTTPException, status


class ApiException(HTTPException):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(status_code=status_code, detail={"code": code, "message": message})


class NotFoundException(ApiException):
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, "NOT_FOUND", message)


class ValidationException(ApiException):
    def __init__(self, message: str = "Validation failed") -> None:
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, "VALIDATION_ERROR", message)


class UnauthorizedException(ApiException):
    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED", message)


class ForbiddenException(ApiException):
    def __init__(self, message: str = "Access forbidden") -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, "FORBIDDEN", message)


class ConflictException(ApiException):
    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(status.HTTP_409_CONFLICT, "CONFLICT", message)
