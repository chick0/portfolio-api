from fastapi import APIRouter
from fastapi import HTTPException

from sql import get_session
from sql.models import Project
from v3.project.models import ProjectDetail
from v3.storage.utils import to_date

router = APIRouter()


@router.get(
    "/{project_uuid}",
    description="프로젝트 정보를 불러옵니다.",
    response_model=ProjectDetail
)
async def project_detail(project_uuid: str):
    session = get_session()
    project: Project = session.query(Project).filter_by(
        uuid=project_uuid
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail={
                "alert": "해당 프로젝트를 찾지 못했습니다."
            }
        )

    session.close()

    return ProjectDetail(
        uuid=project.uuid,
        title=project.title,
        date=to_date(
            date=project.date
        ),
        tags=[
            x
            for x in [x.strip() for x in project.tag.split(",")]
            if len(x) != 0
        ],
        web=project.web,
        github=project.github,
        a=project.a,
        b=project.b,
        c=project.c
    )
