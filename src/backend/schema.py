from dataclasses import dataclass, asdict, field
from typing import List
import json

shcema_config = json.load(open("configs/schema.json", "r"))


class BaseRecord:
    def __init__(self, key, **kwargs):
        self.key = key
        for k_, v_ in kwargs.items():
            setattr(self, k_, v_)

    def to_dict(self):
        attributes = [
            a
            for a in self.__dir__()
            if not a.startswith("__") and not callable(getattr(self, a))
        ]
        return {a: getattr(self, a) for a in attributes}


def create_dataclass(name):
    @dataclass
    class BaseRecord:
        def __init__(self, **kwargs):
            for k_, v_ in kwargs.items():
                # setattr(self, "_" + k_, None)
                # setattr(self, k_, v_['default'])
                print(k_, v_)
                setattr(self, k_, v_)

        def to_dict(self):
            return {k: v for k, v in asdict(self).items()}

    return BaseRecord


SCHEMA_FACTORY = {}

for item in shcema_config:
    # attrs = {}
    # for key, value in item.items():
    #     if key != "name":
    #         attrs[key] = eval(value)
    # print(attrs)
    # SCHEMA_FACTORY[item["name"]] = dataclass(type(item["name"]), **attrs)
    # print(item)
    # name = item.pop("name")
    name = item["name"]
    # print(item)
    SCHEMA_FACTORY[name] = create_dataclass(name)


# @dataclass
# class ExpertValidity:
#     expert_id: int
#     score: float
#     created_at: str


# @dataclass
# class Record:
#     key: int  # explicit dataset key
#     record_id: int
#     patient_id: int
#     vitals: str
#     unit: str
#     loinc_code: str
#     vitals_reading: float
#     body_position: str
#     user_type: str
#     record_created_by: str
#     datetime_record_created: str
#     record_updated_by: str
#     datetime_record_deleted: str
#     record_validity: int
#     timestamp: int
#     vitals_type: str
#     expert_validity: List[ExpertValidity] = field(default_factory=lambda: [])
#     # for i in range(1, 11):
#     #     expert_validity.append(ExpertValidity(i, 0.9, "2021-09-01T00:00:00.000Z"))

#     def to_dict(self):
#         return {k: v for k, v in asdict(self).items()}


if __name__ == "__main__":
    # Record = SCHEMA_FACTORY["Record"]
    # print(dir(Record))
    record = BaseRecord(
        key="key_1", data={"data1": "value1", "data2": "value2"}
    )
    print(record.to_dict())
    # record = BaseRecord({"data1": "value1", "data2": "value2"})
    # print(record)
