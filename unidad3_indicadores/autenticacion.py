import bcrypt

class Auth:
    @staticmethod
    def hash_password(password: str) -> bytes:
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password_bytes, salt)

    @staticmethod
    def verify_password(password: str, hashed: bytes) -> bool:
        password_bytes = password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed)

