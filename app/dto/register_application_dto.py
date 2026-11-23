from pydantic import BaseModel, ConfigDict

class RegisterApplicationDto(BaseModel):
    app_name: str