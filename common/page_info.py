from pydantic import BaseModel, conint


class Page(BaseModel):
    page: conint(ge=1) = 1  # 页码，默认为 1，最小值为 1
    size: conint(ge=1, le=100) = 20  # 每页大小，默认 20，最大 100
