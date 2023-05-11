from dataclasses import dataclass, asdict, field
from typing import List, Optional
import json
from typing import Dict, Type, TypeVar
from copy import deepcopy
import streamlit_authenticator as stauth

schema_config = json.load(open("configs/schema.json", "r"))


class BaseRecord:
    def __init__(self, key, /, **kwargs):
        self.key = key
        for k_, v_ in kwargs.items():
            setattr(self, k_, v_)

    def to_dict(self):
        d = deepcopy(vars(self))
        return d


def create_dataclass():
    return BaseRecord


SCHEMA_FACTORY = {}

for item in schema_config:
    name = item.pop("name")
    SCHEMA_FACTORY[name] = create_dataclass()


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
        d = deepcopy(vars(self))
        return d


# TODO: Replace this with dynamically created Schema from app config


@dataclass
class ExpertValidity:
    expert_id: int
    score: float
    created_at: str


@dataclass
class Record:
    key: int  # explicit dataset key
    record_id: int
    patient_id: int
    vitals: str
    unit: str
    loinc_code: str
    vitals_reading: float
    body_position: str
    user_type: str
    record_created_by: str
    datetime_record_created: str
    record_updated_by: str
    datetime_record_deleted: str
    record_validity: int
    timestamp: int
    vitals_type: str
    expert_validity: List[ExpertValidity] = field(default_factory=lambda: [])

    def to_dict(self):
        return {k: v for k, v in asdict(self).items()}


if __name__ == "__main__":
    print(SCHEMA_FACTORY)
    pass
