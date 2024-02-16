from enum import Enum


class LemmyPostSort(Enum):
    HOT = 'Hot'
    ACTIVE = 'Active'
    NEW = 'New'
    OLD = 'Old'
    TOP = 'Top'
    CONTROVERSIAL = 'Controversial'
    MOSTCOMMENTS = 'MostComments'
    NEWCOMMENTS = 'NewComments'
