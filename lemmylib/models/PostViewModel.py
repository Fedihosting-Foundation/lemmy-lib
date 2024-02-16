from typing import Optional, Any

from lemmylib.models.BaseModel import BaseModel
from lemmylib.models.PostModel import PostModel


class PostViewModel(BaseModel):
    post: PostModel

    def __init__(self, **data):
        if "post" in data:
            if not isinstance(data["post"], PostModel):
                data["post"] = PostModel(**data["post"])
        else:
            raise ValueError("PostViewModel requires a PostModel object")
        super().__init__(**data)
