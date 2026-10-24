class AuthServiceError(Exception):
    """Base exception for authentication errors."""


class InvalidCredentialsError(AuthServiceError):
    pass


class EmailAlreadyExistsError(AuthServiceError):
    pass


class PatientNotFoundError(AuthServiceError):
    pass


class InvalidRefreshTokenError(AuthServiceError):
    pass


class RefreshTokenReuseError(AuthServiceError):
    pass