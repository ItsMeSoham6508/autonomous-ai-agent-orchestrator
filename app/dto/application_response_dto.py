from pydantic import BaseModel, ConfigDict


class ApplicationResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    app_name: str | None
    api_key: str | None
