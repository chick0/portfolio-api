from collections import namedtuple


User = namedtuple(
    "User",
    "github_id"
)

Github = namedtuple(
    "Github",
    "client_id client_secret"
)

Database = namedtuple(
    "Database",
    "host port user password database"
)


##############################################
del namedtuple
__all__ = [model for model in dir() if not model.startswith("__")]
