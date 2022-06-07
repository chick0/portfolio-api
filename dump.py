from time import time
from json import dump

from dotenv import load_dotenv

from sql import get_session
from sql.models import Project


def main():
    load_dotenv()
    session = get_session()
    result = []

    for project in session.query(Project).all():
        result.append({
            "uuid": project.uuid,
            "title": project.title,
            "date": project.date.timestamp(),
            "tag": project.tag,
            "web": project.web,
            "github": project.github,
            "a": project.a,
            "b": project.b,
            "c": project.c,
        })

    dump(
        obj=result,
        fp=open(f"dump_{round(time())}.json", mode="w", encoding="utf-8"),
        indent=4,
        ensure_ascii=False,
    )


if __name__ == "__main__":
    main()
