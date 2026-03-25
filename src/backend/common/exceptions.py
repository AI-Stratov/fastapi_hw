class DomainException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsException(DomainException):
    def __init__(self):
        super().__init__("Пользователь с таким именем уже существует")


class UserNotFoundException(DomainException):
    def __init__(self):
        super().__init__("Пользователь не найден")


class InvalidCredentialsException(DomainException):
    def __init__(self):
        super().__init__("Неверное имя пользователя или пароль")


class TaskNotFoundException(DomainException):
    def __init__(self):
        super().__init__("Задача не найдена")
