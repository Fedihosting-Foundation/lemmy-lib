from typing import Optional, Any

from lemmylib.models.BaseModel import BaseModel


class LocalUserModel(BaseModel):
    id: int

    accepted_application: bool
    admin: bool

    email: Optional[str]
    email_verified: bool
