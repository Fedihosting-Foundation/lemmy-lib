from typing import Optional, Any

from lemmylib.models.BaseModel import BaseModel


class CommunityModel(BaseModel):
    id: int

    title: str
    actor_id: str
    description: str
    banner: Optional[str]
    icon: Optional[str]
    local: bool
    nsfw: bool = False

    instance_id: int

    posting_restricted_to_mods: bool

    deleted: bool = False
    removed: bool = False
    hidden: bool = False

    published: str
    updated: Optional[str]
