from pydantic import BaseModel


class UpdateApplicationDto(BaseModel):
    app_name: str
