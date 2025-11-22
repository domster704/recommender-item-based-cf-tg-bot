class DomainError(Exception):
    """Базовый класс для доменных ошибок."""


class UserNotFoundError(DomainError):
    """Пользователь не найден."""


class UserAlreadyExistsError(DomainError):
    """Пользователь уже существует."""
