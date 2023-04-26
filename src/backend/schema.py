from dataclasses import dataclass, asdict, field
from typing import List


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
    expert_validity: List[ExpertValidity] = field(
        default_factory=lambda: [])

    def to_dict(self):
        return {k: v for k, v in asdict(self).items()}


if __name__ == "__main__":
    expert_validity = ExpertValidity(1, 0.9, "2021-09-01T00:00:00.000Z")
    sample_record = Record(1, 1, 1, "BP", "mmHg", "8480-6", 120, "Sitting", "Patient", "Patient", "2021-09-01T00:00:00.000Z",
                           "Patient", "2021-09-01T00:00:00.000Z", 1, 1630454400, "Blood Pressure", [expert_validity])
    print(sample_record.to_dict())

    sample_record = Record(1, 1, 1, "BP", "mmHg", "8480-6", 120, "Sitting", "Patient", "Patient", "2021-09-01T00:00:00.000Z",
                           "Patient", "2021-09-01T00:00:00.000Z", 1, 1630454400, "Blood Pressure")

    print(sample_record.to_dict())
