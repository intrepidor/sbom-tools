import unittest
from jsonschema import ValidationError
from unittest.mock import patch
from readjson import validate_cyclonedx, CYCLONEDX_SCHEMA

# filepath: /Users/allan/Library/Mobile Documents/com~apple~CloudDocs/MyProjects/sbom-tools/test_readjson.py


class TestValidateCycloneDX(unittest.TestCase):

    def setUp(self):
        self.valid_cyclonedx = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.2",
            "version": 1,
            "components": [
                {
                    "name": "example-component",
                    "version": "1.0",
                    "description": "An example component",
                    "licenses": [
                        {
                            "license": {
                                "id": "MIT"
                            }
                        }
                    ],
                    "downloadLocation": "https://example.com/download"
                }
            ]
        }

    def test_valid_cyclonedx(self):
        self.assertTrue(validate_cyclonedx(self.valid_cyclonedx))

    def test_missing_required_field(self):
        invalid_cyclonedx = self.valid_cyclonedx.copy()
        del invalid_cyclonedx["bomFormat"]
        self.assertFalse(validate_cyclonedx(invalid_cyclonedx))

    def test_incorrect_field_type(self):
        invalid_cyclonedx = self.valid_cyclonedx.copy()
        invalid_cyclonedx["version"] = "1"  # Should be an integer
        self.assertFalse(validate_cyclonedx(invalid_cyclonedx))

    def test_incorrect_field_pattern(self):
        invalid_cyclonedx = self.valid_cyclonedx.copy()
        invalid_cyclonedx["specVersion"] = "2.0"  # Should match "^1\\.2$"
        self.assertFalse(validate_cyclonedx(invalid_cyclonedx))

    @patch('readjson.logging.error')
    def test_logging_on_validation_error(self, mock_logging_error):
        invalid_cyclonedx = self.valid_cyclonedx.copy()
        del invalid_cyclonedx["bomFormat"]
        validate_cyclonedx(invalid_cyclonedx)
        mock_logging_error.assert_called_once()

if __name__ == '__main__':
    unittest.main()