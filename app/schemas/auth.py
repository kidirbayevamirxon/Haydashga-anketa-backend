from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ParticipantStartRequest(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)


class ParticipantStartResponse(BaseModel):
    id: str
    first_name: str
    last_name: str