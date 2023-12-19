from typing import Any, Optional

from lemmylib.lib import LemmyLib
from lemmylib.entities.PersonEntity import PersonEntity
from lemmylib.models.PostModel import PostModel


class PostEntity:
    data: PostModel = None

    def __init__(self, data: PostModel, client: LemmyLib):
        self.data = data
        self.client = client

    def get_id(self) -> int:
        return self.data.id

    def get_local(self) -> bool:
        return self.data.local

    def get_embed_title(self) -> Optional[str]:
        return self.data.embed_title

    def get_embed_description(self) -> Optional[str]:
        return self.data.embed_description

    def get_embed_video_url(self) -> Optional[str]:
        return self.data.embed_video_url

    def get_thumbnail_url(self) -> Optional[str]:
        return self.data.thumbnail_url

    def get_url(self) -> Optional[str]:
        return self.data.url

    def get_featured_community(self) -> bool:
        return self.data.featured_community

    def get_featured_local(self) -> bool:
        return self.data.featured_local

    def get_published(self) -> str:
        return self.data.published

    def get_updated(self) -> str:
        return self.data.updated

    def get_deleted(self) -> bool:
        return self.data.deleted

    def get_removed(self) -> bool:
        """
        Remove = Mod removed this post
        """
        return self.data.removed

    def get_name(self) -> str:
        return self.data.name

    def get_title(self) -> str:
        return self.get_name()

    def get_creator_id(self) -> int:
        return self.data.creator_id

    def get_creator(self) -> PersonEntity:
        return self.client.get_person(self.get_creator_id())

    def get_app_id(self) -> str:
        return self.data.ap_id

    def get_body(self) -> str:
        return self.data.body

    def get_data(self) -> PostModel:
        return self.data

    def get_client(self) -> LemmyLib:
        return self.client

    def remove(self, reason: str | None = None) -> bool:
        if self.get_removed() or self.get_deleted() or self.get_id() is None:
            return False
        self.client.remove_post(self.get_id(), reason, True)
        return True

    def restore(self, reason: str | None = None) -> bool:
        if not self.get_removed() or self.get_deleted() or self.get_id() is None:
            return False
        self.client.remove_post(self.get_id(), reason, False)
        return True

    def get_community_id(self) -> int:
        return self.data.community_id

    # Todo: Add community entity
    def get_community(self) -> Any:
        return self.client.get_community(self.get_community_id())

    def get_nsfw(self) -> bool:
        return self.data.nsfw
