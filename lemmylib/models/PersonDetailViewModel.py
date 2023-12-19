from typing import Optional, Any

from lemmylib.models.BaseModel import BaseModel
from lemmylib.models.PersonModel import PersonModel


class PersonViewModel(BaseModel):

    def __init__(self, **data):
        if "person" in data:
            if not isinstance(data["person"], PersonModel):
                data["person"] = PersonModel(**data["person"])
        else:
            raise ValueError("PersonViewModel requires a PersonModel object")
        super().__init__(**data)

    counts: Any
    is_admin: bool
    person: PersonModel
