from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return context.hash(password)