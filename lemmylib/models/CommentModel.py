from typing import Optional, Any

from lemmylib.models.BaseModel import BaseModel


class CommentModel(BaseModel):
    id: int

    ap_id: str
    local: bool
    creator_id: int
    post_id: int
    content: str = ""
    published: str
    deleted: bool = False
    removed: bool = False
    language_id: int
    updated: Optional[str]
