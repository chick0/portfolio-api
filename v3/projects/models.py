from pydantic import BaseModel


class ProjectPreview(BaseModel):
    uuid: str
    title: str
    date: str
    tags: list[str]


class PageData(BaseModel):
    this: int
    max: int


class ProjectList(BaseModel):
    projectList: list[ProjectPreview]
    page: PageData
