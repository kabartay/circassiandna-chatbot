#!/usr/bin/env python

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

import logging
import re
from typing import Optional


def remove_trailing_commas(text: str) -> str:
    """
    Remove trailing commas before } or ] in a JSON string.
    """
    # Remove comma before }
    text = re.sub(r",\s*}", "}", text)
    # Remove comma before ]
    text = re.sub(r",\s*]", "]", text)
    return text


def get_module_logger(mod_name: Optional[str] = None) -> logging.Logger:
    """
    Create and configure a logger for multi-module usage.
    :param mod_name: The name of the logger. If None, the root logger is used.
    :return: A configured logger instance.
    """
    logger = logging.getLogger(mod_name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger
