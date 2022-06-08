from secrets import token_bytes

FILE = ".JWT_SECRET"


def get() -> str:
    with open(FILE, mode="rb") as reader:
        return reader.read().hex()


def create() -> None:
    with open(FILE, mode="wb") as writer:
        writer.write(token_bytes(32))

    print("* NEW SECRET GENERATED *")
