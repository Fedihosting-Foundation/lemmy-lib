from typing import Any


class BaseModel:

    def __init__(self, **data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


    def __getitem__(self, key: Any) -> Any:
        return self[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self[key] = value

    def __delitem__(self, key: Any) -> None:
        del self[key]
