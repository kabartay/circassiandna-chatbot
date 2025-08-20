#!/usr/bin/env python3

"""
Copyright (C) 2025 Mukharbek Organokov
Website: www.circassiandna.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
from pathlib import Path
from typing import List

from utils import get_module_logger, remove_trailing_commas

LOGGER = get_module_logger(__name__)


def combine_json_files(
    input_dir: str, input_files: List[str], output_file: str
) -> None:
    """
    Combine multiple JSON dict files from a directory into one JSON file.
    :param input_dir: Directory containing JSON files.
    :param input_files: List of JSON file paths to combine.
    :param output_file: Path to the output combined JSON file.
    """
    combined_data = {}

    dirpath = Path(input_dir)
    if not dirpath.is_dir():
        LOGGER.error("Directory does not exist: %s", input_dir)
        return

    for filename in input_files:
        filepath = dirpath / filename
        if not filepath.is_file():
            LOGGER.warning("File not found, skipping: %s", filepath)
            continue

        try:
            # Read raw text
            raw_text = filepath.read_text(encoding="utf-8")
            # Fix trailing commas
            fixed_text = remove_trailing_commas(raw_text)
            # Parse JSON
            data = json.loads(fixed_text)
            if not isinstance(data, dict):
                LOGGER.warning(
                    "Skipping %s: not a JSON object at top level", filepath
                )
                continue
            combined_data.update(data)
            LOGGER.info("Added %s", filepath)
        except json.JSONDecodeError as err:
            LOGGER.error("Invalid JSON in %s: %s", filepath, err)
        except Exception as err:
            LOGGER.error("Error reading %s: %s", filepath, err)

    if combined_data:
        try:
            # output_dir = os.path.dirname(output_file)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(combined_data, f, indent=2, ensure_ascii=False)
            LOGGER.info("Combined JSON saved to %s", output_file)
        except Exception as err:
            LOGGER.error(
                "Failed to write output file %s: %s", output_file, err
            )
    else:
        LOGGER.warning("No valid JSON data to write.")


def main() -> None:
    """
    Main entry point for the script.
    - Looks for explicit list of `.json` files in a INPUT_DIR directory.
    - Expects each file to contain a JSON object (dict at top-level).
    - Handles missing files and invalid JSON gracefully.
    - Merges all dicts into one combined dict.
    - Saves the result into OUTPUT_FILE.
    """

    input_dir = "data"
    files_to_combine = [
        "base.json",
        "ftdna.json",
        "order.json",
        "hg.json",
        "projects.json",
        "tree.json",
        "genealogy.json",
        "general.json",
        "miscellaneous.json",
    ]
    output_path = "knowledgebase.json"
    combine_json_files(input_dir, files_to_combine, output_path)


if __name__ == "__main__":
    main()
