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


def check_subdirs(input_dir: str, required_subdirs: str) -> bool:
    """
    Checks directory structure.
    :param input_dir: An input directory. Default is data.
    :param required_subdirs: A list of required subdirectories.
    :return: Boolean.
    """
    missing_subdirs = []
    dirpath = Path(input_dir)

    if not dirpath.is_dir():
        LOGGER.error("Directory does not exist: %s", input_dir)
        return False

    for sub in required_subdirs:
        subdir = dirpath / sub
        if not subdir.is_dir():
            missing_subdirs.append(subdir)

    if missing_subdirs:
        for m in missing_subdirs:
            LOGGER.error("Missing required subdir: %s", m)
        return False

    return True


def combine_json_files(
    input_dir: str,
    required_subdirs: str,
    input_filenames: List[str],
    output_file: str,
) -> None:
    """
    Combine multiple JSON dict files from a directory into one JSON file.
    :param input_dir: Directory containing JSON files.
    :param input_filenames: List of JSON file names to combine.
    :param output_file: Path to the output combined JSON file.
    """
    combined_data = {}
    if check_subdirs(input_dir=input_dir, required_subdirs=required_subdirs):
        LOGGER.info("All required subdirectories exist!")

        dirpath = Path(input_dir)
        for sub in required_subdirs:
            for filename in input_filenames:
                filepath = dirpath / sub / f"{filename}_{sub}.json"
                if not filepath.is_file():
                    LOGGER.warning("File not found, skipping: %s", filepath)
                    continue

                try:
                    read_raw_text = filepath.read_text(encoding="utf-8")
                    fixed_text = remove_trailing_commas(read_raw_text)
                    data = json.loads(fixed_text)
                    if not isinstance(data, dict):
                        LOGGER.warning(
                            "Skipping %s: not a JSON object at top level",
                            filepath,
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
                        json.dump(
                            combined_data, f, indent=2, ensure_ascii=False
                        )
                    LOGGER.info("Combined JSON saved to %s", output_file)
                except Exception as err:
                    LOGGER.error(
                        "Failed to write output file %s: %s", output_file, err
                    )
            else:
                LOGGER.warning("No valid JSON data to write.")

    else:
        LOGGER.error(
            "Aborting combine: required subdirectories %s not found in %s",
            required_subdirs,
            input_dir,
        )


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
    required_subdirs = ["en", "ru"]
    input_filenames = [
        "base",
        "ftdna",
        "order",
        "hg",
        "archeology",
        "history",
        "projects",
        "tree",
        "genealogy",
        "general",
        "miscellaneous",
    ]
    output_path = "knowledgebase.json"
    combine_json_files(
        input_dir, required_subdirs, input_filenames, output_path
    )


if __name__ == "__main__":
    main()
