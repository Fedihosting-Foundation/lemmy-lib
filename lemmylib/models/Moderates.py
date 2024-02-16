from lemmylib.models.BaseModel import BaseModel
from lemmylib.models.CommunityModel import CommunityModel
from lemmylib.models.PersonModel import PersonModel


class Moderates(BaseModel):
    community: CommunityModel
    person: PersonModel
