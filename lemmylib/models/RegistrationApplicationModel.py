from typing import Optional, Any

from lemmylib.entities.PersonEntity import PersonEntity
from lemmylib.models.BaseModel import BaseModel
from lemmylib.models.LocalUserModel import LocalUserModel


class RegistrationApplicationModel(BaseModel):
    id: int

    admin_id: int
    answer: str
    deny_reason: Optional[str]
    local_user_id: int
    published: str


class RegistrationApplicationViewModel(BaseModel):
    def __init__(self, **data):
        if data.get("application") is not None:
            if not isinstance(data.get("application"), RegistrationApplicationModel):
                data["application"] = RegistrationApplicationModel(**data["application"])
        else:
            raise Exception("RegistrationApplicationViewModel: application is None")

        super().__init__(**data)

    id: int
    creator: PersonEntity
    creator_local_user: LocalUserModel
    admin: Optional[PersonEntity]
    application: RegistrationApplicationModel
