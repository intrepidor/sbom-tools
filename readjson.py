"""
Module: readjson

This module provides functionality to convert between CycloneDX and SPDX SBOM formats.
It includes functions to read, write, and transfer data between these formats, as well as
a command-line interface to perform these conversions.

Dependencies:
- json
- argparse
- logging
- typing
- jsonschema

Usage:
    python readjson.py --cyclonedx-to-spdx input_file output_file
    python readjson.py --spdx-to-cyclonedx input_file output_file
    python readjson.py --validate-cyclonedx input_file
    python readjson.py --validate-spdx input_file
    python readjson.py --log-level 5
    python readjson.py --version
"""

import json
import argparse
import logging
from typing import Any, Dict, List
from jsonschema import validate, ValidationError

# CycloneDX and SPDX schemas
CYCLONEDX_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "CycloneDX 1.2 Schema",
    "type": "object",
    "properties": {
        "bomFormat": {
            "type": "string",
            "pattern": "^CycloneDX$"
        },
        "specVersion": {
            "type": "string",
            "pattern": "^1\\.2$"
        },
        "version": {
            "type": "integer"
        },
        "components": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "version": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    },
                    "licenses": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "license": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "string"
                                        }
                                    },
                                    "required": ["id"]
                                }
                            },
                            "required": ["license"]
                        }
                    },
                    "downloadLocation": {
                        "type": "string"
                    }
                },
                "required": ["name"]
            }
        }
    },
    "required": ["bomFormat", "specVersion", "version"]
}

SPDX_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "SPDX 3.0.1 Schema",
    "type": "object",
    "properties": {
        "spdxVersion": {
            "type": "string",
            "pattern": "^SPDX-3\\.0\\.1$"
        },
        "dataLicense": {
            "type": "string"
        },
        "documentNamespace": {
            "type": "string",
            "format": "uri"
        },
        "name": {
            "type": "string"
        },
        "version": {
            "type": "string"
        },
        "creationInfo": {
            "type": "object",
            "properties": {
                "created": {
                    "type": "string",
                    "format": "date-time"
                },
                "creators": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "licenseListVersion": {
                    "type": "string"
                }
            },
            "required": ["created", "creators"]
        },
        "packages": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "spdxId": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string"
                    },
                    "version": {
                        "type": "string"
                    },
                    "downloadLocation": {
                        "type": "string"
                    },
                    "licenseConcluded": {
                        "type": "string"
                    },
                    "licenseInfoFromFiles": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "description": {
                        "type": "string"
                    }
                },
                "required": ["spdxId", "name"]
            }
        }
    },
    "required": ["spdxVersion", "dataLicense", "documentNamespace", "name", "version", "creationInfo"]
}

def transfer_data_to_spdx(cyclone_d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transfer data from CycloneDX format to SPDX format.

    Args:
        cyclone_d (Dict[str, Any]): The CycloneDX data.

    Returns:
        Dict[str, Any]: The SPDX data.
    """
    spdx: Dict[str, Any] = {
        "spdxVersion": "SPDX-2.2",
        "dataLicense": "CC0-1.0",
        "documentNamespace": "http://spdx.org/spdxdocs/example-spdx-document",
        "name": "Example SPDX Document",
        "version": "1.0",
        "creationInfo": {
            "created": "2023-10-01T00:00:00Z",
            "creators": ["Tool: readjson"],
            "licenseListVersion": "3.0"
        },
        "packages": []
    }

    for component in cyclone_d.get('components', []):
        spdx['packages'].append({
            "spdxId": f"SPDXRef-{component['name']}",
            "name": component['name'],
            "version": component.get('version', 'unknown'),
            "downloadLocation": component.get('downloadLocation', 'NOASSERTION'),
            "licenseConcluded": component.get('license', 'NOASSERTION'),
            "licenseInfoFromFiles": component.get('licenses', []),
            "description": component.get('description', 'NOASSERTION')
        })

    return spdx

def transfer_data_to_cyclonedx(spdx_d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transfer data from SPDX format to CycloneDX format.

    Args:
        spdx_d (Dict[str, Any]): The SPDX data.

    Returns:
        Dict[str, Any]: The CycloneDX data.
    """
    cyclonedx: Dict[str, Any] = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.2",
        "version": 1,
        "components": []
    }

    for package in spdx_d.get('packages', []):
        cyclonedx['components'].append({
            "name": package['name'],
            "version": package.get('version', 'unknown'),
            "downloadLocation": package.get('downloadLocation', 'NOASSERTION'),
            "licenses": package.get('licenseInfoFromFiles', []),
            "description": package.get('description', 'NOASSERTION')
        })

    return cyclonedx

def write_spdx_file(spdx: Dict[str, Any], output_path: str) -> None:
    """
    Write SPDX data to a file.

    Args:
        spdx (Dict[str, Any]): The SPDX data.
        output_path (str): The output file path.
    """
    with open(output_path, 'w') as file:
        json.dump(spdx, file, indent=4)

def write_cyclonedx_file(cyclonedx: Dict[str, Any], output_path: str) -> None:
    """
    Write CycloneDX data to a file.

    Args:
        cyclonedx (Dict[str, Any]): The CycloneDX data.
        output_path (str): The output file path.
    """
    with open(output_path, 'w') as file:
        json.dump(cyclonedx, file, indent=4)

def read_cyclonedx_file(file_path: str) -> Dict[str, Any]:
    """
    Read CycloneDX data from a file.

    Args:
        file_path (str): The file path.

    Returns:
        Dict[str, Any]: The CycloneDX data.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def read_spdx_file(file_path: str) -> Dict[str, Any]:
    """
    Read SPDX data from a file.

    Args:
        file_path (str): The file path.

    Returns:
        Dict[str, Any]: The SPDX data.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def validate_cyclonedx(cyclone_d: Dict[str, Any]) -> bool:
    """
    Validate CycloneDX data against the CycloneDX schema.

    Args:
        cyclone_d (Dict[str, Any]): The CycloneDX data.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        validate(instance=cyclone_d, schema=CYCLONEDX_SCHEMA)
        return True
    except ValidationError as e:
        logging.error(f"CycloneDX validation error: {e}")
        return False

def validate_spdx(spdx_d: Dict[str, Any]) -> bool:
    """
    Validate SPDX data against the SPDX schema.

    Args:
        spdx_d (Dict[str, Any]): The SPDX data.

    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        validate(instance=spdx_d, schema=SPDX_SCHEMA)
        return True
    except ValidationError as e:
        logging.error(f"SPDX validation error: {e}")
        return False


def validate_purl(purl: str) -> bool:
    """
    Validate a Package URL (PURL).

    Args:
        purl (str): The PURL to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    import re
    pattern = re.compile(r'^pkg:(?P<type>.+)/(?P<name>.+)@(?P<version>.+)$')
    return bool(pattern.match(purl))


def validate_cpe_string(cpe: str) -> bool:
    """
    Validate a Common Platform Enumeration (CPE) string.

    Args:
        cpe (str): The CPE string to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    import re
    pattern = re.compile(r'^cpe:2\.3:'
                         r'(?P<part>o|h):'
                         r'(?P<vendor>[^:]*):'
                         r'(?P<product>[^:]*):'
                         r'(?P<version>[^:]*):'
                         r'(?P<update>[^:]*):'
                         r'(?P<edition>[^:]*):'
                         r'(?P<language>[^:]*):'
                         r'(?P<sw_edition>[^:]*):'
                         r'(?P<target_sw>[^:]*):'
                         r'(?P<target_hw>[^:]*):'
                         r'(?P<other>.*)$')
    return bool(pattern.match(cpe))

def main() -> None:
    """
    Main function to handle command line arguments and perform conversions.
    """
    parser = argparse.ArgumentParser(description="Convert between CycloneDX and SPDX SBOM formats.")
    parser.add_argument('--input', metavar='input', help="Input file")
    parser.add_argument('--output', metavar='output', help="Output file")
    parser.add.argument('--format', choices=['CycloneDX', 'SPDX'], help="Output format (CycloneDX or SPDX)")
    parser.add_argument('--validate-cyclonedx', metavar='input', help="Validate CycloneDX input file")
    parser.add.argument('--validate-spdx', metavar='input', help="Validate SPDX input file")
    parser.add.argument('--log-level', type=int, choices=range(1, 10), help="Set logging level (1-9)")
    parser.add.argument('--version', action='version', version='readjson 1.0')

    args = parser.parse_args()

    # Set up logging
    log_level = logging.WARNING
    if args.log_level:
        log_level = 10 - args.log_level
    logging.basicConfig(level=log_level)

    if args.validate_cyclonedx:
        input_file = args.validate_cyclonedx
        logging.info(f"Validating CycloneDX file {input_file}")
        cyclone_d = read_cyclonedx_file(input_file)
        if validate_cyclonedx(cyclone_d):
            logging.info("CycloneDX validation successful")
        else:
            logging.error("CycloneDX validation failed")

    elif args.validate_spdx:
        input_file = args.validate_spdx
        logging.info(f"Validating SPDX file {input_file}")
        spdx_d = read_spdx_file(input_file)
        if validate_spdx(spdx_d):
            logging.info("SPDX validation successful")
        else:
            logging.error("SPDX validation failed")

    elif args.input and args.output and args.format:
        input_file = args.input
        output_file = args.output
        output_format = args.format

        if output_format == 'SPDX':
            logging.info(f"Converting CycloneDX file {input_file} to SPDX file {output_file}")
            cyclone_d = read_cyclonedx_file(input_file)
            spdx = transfer_data_to_spdx(cyclone_d)
            write_spdx_file(spdx, output_file)
            logging.info("Conversion to SPDX completed successfully")

        elif output_format == 'CycloneDX':
            logging.info(f"Converting SPDX file {input_file} to CycloneDX file {output_file}")
            spdx_d = read_spdx_file(input_file)
            cyclonedx = transfer_data_to_cyclonedx(spdx_d)
            write_cyclonedx_file(cyclonedx, output_file)
            logging.info("Conversion to CycloneDX completed successfully")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
