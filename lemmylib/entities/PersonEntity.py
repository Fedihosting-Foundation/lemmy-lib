from typing import Any, Self, Optional

from lemmylib.lib import LemmyLib
from lemmylib.models.CommentModel import CommentModel
from lemmylib.models.PersonModel import PersonModel


class PersonEntity:
    data: PersonModel = None

    def __init__(self, data: PersonModel, client: LemmyLib):
        self.data = data
        self.client = client

    def get_id(self) -> int:
        return self.data.id

    def get_local(self) -> bool:
        return self.data.local

    def get_updated(self) -> str:
        return self.data.updated

    def get_deleted(self) -> bool:
        return self.data.deleted

    def get_banned(self) -> bool:
        return self.data.banned

    def get_ban_expires(self) -> Optional[str]:
        return self.data.ban_expires

    def get_name(self) -> str:
        return self.data.name

    def get_display_name(self) -> Optional[str]:
        return self.data.display_name

    def get_bio(self) -> Optional[str]:
        return self.data.bio

    def get_actor_id(self) -> str:
        return self.data.actor_id

    def get_matrix_user_id(self) -> Optional[str]:
        return self.data.matrix_user_id

    def get_avatar(self) -> Optional[str]:
        return self.data.avatar

    def get_banner(self) -> Optional[str]:
        return self.data.banner

    def get_created(self) -> str:
        return self.data.created

    def get_instance_id(self) -> int:
        return self.data.instance_id

    def get_bot_account(self) -> bool:
        return self.data.bot_account

    def get_data(self) -> PersonModel:
        return self.data

    def get_client(self) -> LemmyLib:
        return self.client

    def ban(self, reason: str | None = None, expires: str | None = None, remove_data: bool = False) -> bool:
        if self.get_banned() or self.get_deleted() or self.get_id() is None:
            return False
        self.client.ban_person(self.get_id(), reason, expires, remove_data)
        return True

    def unban(self, reason: str | None = None) -> bool:
        if not self.get_banned() or self.get_deleted() or self.get_id() is None:
            return False
        self.client.ban_person(self.get_id(), reason, banned=False)
        return True

    def remove(self, reason: str | None = None, remove: bool = True) -> bool:
        if self.get_banned() or self.get_deleted() or self.get_id() is None:
            return False
        self.client.remove_comment(self.get_id(), reason, remove)
        return True

    def purge(self, reason: str | None = None) -> bool:
        self.client.purge_person(self.get_id(), reason)
        return True


