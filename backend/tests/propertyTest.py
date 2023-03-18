import unittest
from unittest.mock import patch, MagicMock
from services.property import PropertyService


class TestPropertyService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.property_service = PropertyService()

    def test_get_all_properties(self):
        expected_result = [
            {
                "id": 1,
                "address": "123 Main St.",
                "price": 100000,
                "description": "A beautiful house in the suburbs.",
            },
            {
                "id": 2,
                "address": "456 Elm St.",
                "price": 150000,
                "description": "A spacious apartment in the city.",
            },
        ]
        mock_property_model = MagicMock()
        mock_property_model.query.all.return_value = expected_result
        with patch("app.services.property.PropertyModel", mock_property_model):
            result = self.property_service.get_all_properties()
            self.assertEqual(result, expected_result)

    def test_get_property_by_id(self):
        expected_result = {
            "id": 1,
            "address": "123 Main St.",
            "price": 100000,
            "description": "A beautiful house in the suburbs.",
        }
        mock_property_model = MagicMock()
        mock_property_model.query.get.return_value = expected_result
        with patch("app.services.property.PropertyModel", mock_property_model):
            result = self.property_service.get_property_by_id(1)
            self.assertEqual(result, expected_result)

    def test_get_active_properties(self):
        expected_result = [
            {
                "id": 1,
                "address": "123 Main St.",
                "price": 100000,
                "description": "A beautiful house in the suburbs.",
                "event_id": 1,
            }
        ]
        mock_property_model = MagicMock()
        mock_property_model.query.filter.return_value.join.return_value.filter.return_value.all.return_value = (
            expected_result
        )
        with patch("app.services.property.PropertyModel", mock_property_model):
            result = self.property_service.get_active_properties()
            self.assertEqual(result, expected_result)

    def test_create_property(self):
        property_data = {
            "address": "789 Oak St.",
            "price": 200000,
            "description": "A cozy cottage in the woods.",
        }
        mock_property_model = MagicMock()
        with patch("app.services.property.PropertyModel", mock_property_model):
            result = self.property_service.create_property(property_data)
            self.assertTrue(result)

    def test_update_property(self):
        property_data = {
            "id": 1,
            "address": "123 Main St.",
            "price": 150000,
            "description": "A beautiful house in the suburbs.",
        }
        mock_property_model = MagicMock()
        with patch("app.services.property.PropertyModel", mock_property_model):
            result = self.property_service.update_property(property_data)
            self.assertTrue(result)

    def test_delete_property(self):
        mock_property_model = MagicMock()
        with patch("app.services.property.PropertyModel", mock_property_model):
            result = self.property_service.delete_property(1)
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
