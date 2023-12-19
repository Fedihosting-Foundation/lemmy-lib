from typing import Optional, Any

from lemmylib.models.BaseModel import BaseModel


class PostModel(BaseModel):
    id: int
    name: str
    ap_id: str
    creator_id: int
    local: bool
    body: str = ""
    deleted: bool = False
    removed: bool = False
    language_id: int
    nsfw: bool = False
    embed_title: Optional[str]
    embed_description: Optional[str]
    embed_video_url: Optional[str]
    thumbnail_url: Optional[str]
    url: Optional[str]
    community_id: int
    featured_community: bool
    featured_local: bool
    published: str
    updated: Optional[str]
