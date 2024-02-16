from lemmylib.models.BaseModel import BaseModel
from lemmylib.models.CommunityViewModel import CommunityViewModel
from lemmylib.models.Moderates import Moderates
from lemmylib.models.PostViewModel import PostViewModel


class GetPostResponse(BaseModel):
    post_view: PostViewModel
    community_view: CommunityViewModel
    moderators: list[Moderates]
    cross_posts: list[int]

    def __init__(self, **data):
        if "post_view" in data:
            if not isinstance(data["post_view"], PostViewModel):
                data["post_view"] = PostViewModel(**data["post_view"])
        else:
            raise ValueError("GetPostResponse requires a PostViewModel object")
        if "community_view" in data:
            if not isinstance(data["community_view"], CommunityViewModel):
                data["community_view"] = CommunityViewModel(**data["community_view"])
        else:
            raise ValueError("GetPostResponse requires a CommunityViewModel object")
        if "moderators" in data:
            data["moderators"] = [Moderates(**d) for d in data["moderators"]]
        else:
            raise ValueError("GetPostResponse requires a moderators list")
        if "cross_posts" in data:
            data["cross_posts"] = [int(d) for d in data["cross_posts"]]
        else:
            raise ValueError("GetPostResponse requires a cross_posts list")
        super().__init__(**data)
