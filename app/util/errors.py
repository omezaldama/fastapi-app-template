from fastapi import HTTPException, status


class CustomError(HTTPException):
    def __init__(self,
                 message: str = '',
                 code: int = 400,
                 subcode: int = 0):
        super().__init__(status_code=code, detail=message)
        self.message = message
        self.code = code
        self.subcode = subcode


class UnauthorizedError(CustomError):
    def __init__(self,
                 message: str = '',
                 subcode: int = 0):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, subcode)


class ForbiddenError(CustomError):
    def __init__(self,
                 message: str = '',
                 subcode: int = 0):
        super().__init__(message, status.HTTP_403_FORBIDDEN, subcode)


class NotFoundError(CustomError):
    def __init__(self,
                 message: str = '',
                 subcode: int = 0):
        super().__init__(message, status.HTTP_404_NOT_FOUND, subcode)


class ConflictError(CustomError):
    def __init__(self,
                 message: str = '',
                 subcode: int = 0):
        super().__init__(message, status.HTTP_409_CONFLICT, subcode)
