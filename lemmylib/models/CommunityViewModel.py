from typing import Any

from lemmylib.models.BaseModel import BaseModel
from lemmylib.models.CommunityModel import CommunityModel
from lemmylib.models.PersonModel import PersonModel


class CommunityViewModel(BaseModel):

    def __init__(self, **data):
        if "community" in data:
            if not isinstance(data["community"], CommunityModel):
                data["community"] = CommunityModel(**data["community"])
        else:
            raise ValueError("CommunityViewModel requires a CommunityModel object")
        super().__init__(**data)

    community: CommunityModel
