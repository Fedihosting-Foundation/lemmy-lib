from typing import Any, Self, Optional

from lemmylib.lib import LemmyLib
from lemmylib.models.CommentModel import CommentModel
from lemmylib.models.CommunityModel import CommunityModel
from lemmylib.models.PersonModel import PersonModel


class CommentEntity:
    data: CommunityModel = None

    def __init__(self, data: CommunityModel, client: LemmyLib):
        self.data = data
        self.client = client

    def get_id(self) -> int:
        return self.data.id

    def get_local(self) -> bool:
        return self.data.local

    def get_deleted(self) -> bool:
        return self.data.deleted

    def get_removed(self) -> bool:
        return self.data.removed

    def get_hidden(self) -> bool:
        return self.data.hidden

    def get_client(self) -> LemmyLib:
        return self.client

    def get_title(self) -> str:
        return self.data.title

    def get_actor_id(self) -> str:
        return self.data.actor_id

    def get_description(self) -> str:
        return self.data.description

    def get_banner(self) -> Optional[str]:
        return self.data.banner

    def get_icon(self) -> Optional[str]:
        return self.data.icon

    def get_instance_id(self) -> int:
        return self.data.instance_id

    def get_posting_restricted_to_mods(self) -> bool:
        return self.data.posting_restricted_to_mods

    def get_nsfw(self) -> bool:
        return self.data.nsfw

    def get_published(self) -> str:
        return self.data.published

    def get_updated(self) -> Optional[str]:
        return self.data.updated

    def update(self, title: str, description: str, banner: str, icon: str, posting_restricted_to_mods: bool,
               nsfw: bool) -> bool:
        self.client.update_community(
            self.get_id(),
            title,
            description,
            banner,
            icon,
            posting_restricted_to_mods,
            nsfw,
        )
        return True

    def remove(self, reason: str | None = None) -> bool:
        if self.get_removed() or self.get_deleted() or self.get_id() is None:
            return False
        self.client.remove_community(self.get_id(), reason, True)
        return True

    def purge(self, reason: str | None = None) -> bool:
        self.client.purge_community(self.get_id(), reason)
        return True

    def get_data(self) -> CommunityModel:
        return self.data
