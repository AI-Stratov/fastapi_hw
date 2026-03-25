from pydantic import BaseModel


class TokenEntity(BaseModel):
    access_token: str
    token_type: str
    username: str
