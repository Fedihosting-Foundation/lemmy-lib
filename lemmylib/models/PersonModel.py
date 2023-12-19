from typing import Optional, Any

from lemmylib.models.BaseModel import BaseModel


class PersonModel(BaseModel):
    id: int

    name: str
    display_name: Optional[str]

    bio: Optional[str]
    local: bool
    actor_id: str
    matrix_user_id: Optional[str]

    avatar: Optional[str]
    banner: Optional[str]
    ban_expires: Optional[str]
    banned: bool = False
    deleted: bool = False
    instance_id: int
    bot_account: bool = False

    published: str
    updated: Optional[str]
