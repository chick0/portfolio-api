from json import load
from datetime import datetime

from dotenv import load_dotenv

from sql import get_session
from sql.models import Project


def main(target: str):
    load_dotenv()
    session = get_session()
    result = load(
        fp=open(target, mode="r", encoding="utf-8")
    )

    for project in result:
        p = Project()
        p.uuid = project['uuid']
        p.title = project['title']
        p.date = datetime.fromtimestamp(project['date'])
        p.tag = project['tag']
        p.web = project['web']
        p.github = project['github']
        p.a = project['a']
        p.b = project['b']
        p.c = project['c']

        session.add(p)

    session.commit()


if __name__ == "__main__":
    main(target=input("dump_file="))
