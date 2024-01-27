from typing import Dict, List, Tuple


def example_method(
    data: list[Dict], limits: Dict[str]
) -> Tuple[int, List[Dict]]:
    """This is an example method for an expert system method. Your method should should follow this format.

    Args:
        data (list[Dict]): input data. This is a list of dictionaries. Each dictionary represents a record.
        limits (Dict[str]): limits defined by the user for each field in the record.

    Returns:
        Tuple[int, List[Dict]]: Number of relevant records and a list of suspect records.
    """
    return NotImplementedError