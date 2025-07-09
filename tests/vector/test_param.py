import unittest
from vector import param


class TestStruct(unittest.TestCase):
    def test_p1(self):
        json_data = {
            # "resource_id": "123a",
            "collection_name": "123a",
        }
        proj =  param.__ReqBaseCollection(**json_data)
        print(f"proj: {proj}")
        print(f"proj: {proj.project_name}")

        json_output = proj.model_dump(
            by_alias=True,
            exclude_unset=True,
        )
        print(json_output)

        proj2 = param.__ReqBaseCollection(project_name="123a")
        proj2.collection_name = "123b"
        print(f"proj2: {proj2}")
        print(f"proj2: {proj2.model_fields}")
        print(f"proj2: {proj2.model_fields_set}")
