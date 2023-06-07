import json
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Optional

import streamlit_authenticator as stauth
from dacite import from_dict

schema_config = json.load(open("configs/schema.json", "r"))


@dataclass
class AppInfo:
    title: str
    icon: str
    description: str
    subtitle: str
    subtitle_description: str


@dataclass
class SourceValue:
    source: str
    value: str


@dataclass
class FieldDisplay:
    id: str
    type: str
    name: Optional[str] = None
    prefix: Optional[SourceValue] = None
    suffix: Optional[SourceValue] = None


@dataclass
class BlockDisplay:
    type: str
    header: str
    fields: List[FieldDisplay]


@dataclass
class RecordDisplay:
    type: str
    record_id: str
    query_id: str
    blocks: List[BlockDisplay]


@dataclass
class ValidityDisplay:
    type: str
    fields: List[FieldDisplay]


APP_INFO = from_dict(data_class=AppInfo, data=schema_config["app_info"])
RECORD_DISPLAY = from_dict(
    data_class=RecordDisplay, data=schema_config["record"]
)
VALIDITY_DISPLAY = from_dict(
    data_class=ValidityDisplay, data=schema_config["validity"]
)
RECORD_ID = RECORD_DISPLAY.record_id
QUERY_ID = RECORD_DISPLAY.query_id


@dataclass
class User:
    username: str
    password: Optional[str] = None
    name: Optional[str] = None
    model: Optional[str] = None
    key: Optional[str] = None
    is_staff: bool = False
    is_admin: bool = False

    def __post_init__(self):
        self.model = "user"
        if self.name is None:
            self.name = self.username
        if self.key is None:
            self.key = f"user_{self.username}"
        if self.password is not None:
            self.password = stauth.Hasher([self.password]).generate()[0]

    def to_dict(self):
        return deepcopy(vars(self))


if __name__ == "__main__":
    pass
