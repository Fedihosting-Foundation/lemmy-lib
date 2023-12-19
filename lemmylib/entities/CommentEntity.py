from typing import Any, Self

from lemmylib.lib import LemmyLib
from lemmylib.models.CommentModel import CommentModel
from lemmylib.entities.PersonEntity import PersonEntity


class CommentEntity:
    data: CommentModel = None

    def __init__(self, data: CommentModel, client: LemmyLib):
        self.data = data
        self.client = client

    def get_id(self) -> int:
        return self.data.id

    def get_creator_id(self) -> int:
        return self.data.creator_id

    def get_content(self) -> str:
        return self.data.content

    def get_post_id(self) -> int:
        return self.data.post_id

    def get_ap_id(self) -> str:
        return self.data.ap_id

    def get_local(self) -> bool:
        return self.data.local

    def get_published(self) -> str:
        return self.data.published

    def get_updated(self) -> str:
        return self.data.updated

    def get_deleted(self) -> bool:
        return self.data.deleted

    def get_removed(self) -> bool:
        """
           Remove = Mod removed this comment
        """
        return self.data.removed

    def get_language_id(self) -> int:
        return self.data.language_id

    def get_data(self) -> CommentModel:
        return self.data

    def get_client(self) -> LemmyLib:
        return self.client

    def remove(self, reason: str | None = None) -> bool:
        if self.get_removed() or self.get_deleted() or self.get_id() is None:
            return False
        self.client.remove_comment(self.get_id(), reason, True)
        return True

    def restore(self, reason: str | None = None) -> bool:
        if not self.get_removed() or self.get_deleted() or self.get_id() is None:
            return False
        self.client.remove_comment(self.get_id(), reason, False)
        return True

    def purge(self, reason: str | None = None) -> bool:
        self.client.purge_comment(self.get_id(), reason)
        return True

    def update(self, content: str) -> bool:
        if self.get_removed() or self.get_deleted() or self.get_id() is None:
            return False
        self.client.update_comment(self.get_id(), content)
        return True

    def get_creator(self) -> PersonEntity:
        return self.client.get_person(self.get_creator_id())

    def __str__(self) -> str:
        return "CommentEntity: {}".format(self.get_data())

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: Self) -> bool:
        return self.get_id() == other.get_id()

    def __ne__(self, other: Self) -> bool:
        return self.get_id() != other.get_id()

    def __lt__(self, other: Self) -> bool:
        return self.get_id() < other.get_id()

    def __le__(self, other: Self) -> bool:
        return self.get_id() <= other.get_id()

    def __gt__(self, other: Self) -> bool:
        return self.get_id() > other.get_id()

    def __ge__(self, other: Self) -> bool:
        return self.get_id() >= other.get_id()

    def __hash__(self) -> int:
        return hash(self.get_id())

    def __bool__(self) -> bool:
        return self.get_id() is not None

    def __len__(self) -> int:
        return len(self.get_content())

    def __getitem__(self, key: Any) -> Any:
        return self.get_data()[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self.get_data()[key] = value

    def __delitem__(self, key: Any) -> None:
        del self.get_data()[key]
