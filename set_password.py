from getpass import getpass

from app.config import update_config
from app.config.models import User
from app.login import get_user


def main():
    user = input("user: ")
    password = getpass("password: ")

    update_config(
        "User",
        get_user(
            User(
                user=user,
                password=password
            )
        )
    )

    print("password_is_updated")


if __name__ == "__main__":
    main()
