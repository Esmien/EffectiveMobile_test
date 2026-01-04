import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
        Проверяет, совпадает ли пароль с хешем

        Args:
            plain_password (str): Пароль в открытом виде
            hashed_password (str): Хеш пароля

        Returns:
            bool: True, если пароль совпадает с хешем, иначе False
    """

    # Превращаем пароль в набор байтов
    password_bytes = plain_password.encode('utf-8')

    # Проверяем, совпадает ли пароль с хешем
    return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """
        Генерирует хеш пароля

        Args:
            password (str): Пароль в открытом виде

        Returns:
            str: Хеш пароля
    """

    # Превращаем пароль в набор байтов
    password_bytes = password.encode('utf-8')

    # Генерируем соль
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    # Возвращаем хеш в виде строки
    return hashed_password.decode('utf-8')