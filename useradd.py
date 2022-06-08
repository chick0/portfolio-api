from os import environ
from hashlib import sha512

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from sql.models import User


def main():
    def get_password() -> str:
        t = input("password=").strip()
        if len(t) < 8:
            print("**PASSWORD IS TOO SHORT**")
            return get_password()
        else:
            return t

    load_dotenv()
    engine = create_engine(environ['SQLALCHEMY_DATABASE_URI'])
    factory = sessionmaker(bind=engine)

    print("Creating new user!")
    email = input("email=").strip()
    password = get_password()
    password = sha512(password.encode("utf-8")).hexdigest()

    user = User()
    user.email = email
    user.password = password

    session = factory()
    session.add(user)
    session.commit()

    print(user)


if __name__ == "__main__":
    main()
