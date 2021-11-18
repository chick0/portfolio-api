from hashlib import sha384
from hashlib import sha512

from .config import get_config
from .config.models import User


def hash_pw(user: str, password: str) -> str:
    user = sha384(user.encode()).hexdigest()
    target = f"{password}+{user}".encode()
    return sha512(target).hexdigest()


def get_user(user: User = None) -> User:
    if user is None:
        user = get_config("User")

    return User(
        user=sha512(user.user.encode()).hexdigest(),
        password=hash_pw(
            user=user.user,
            password=user.password
        )
    )


def check_login(user: str, password: str) -> bool:
    u = get_user()

    user = sha512(user.encode()).hexdigest()
    password = hash_pw(
        user=user,
        password=password,
    )

    chk1 = u.user == user
    chk2 = u.password == password

    return chk1 and chk2
