from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password):
    new_password = pwd_context.hash(password)
    return new_password
