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

import json
from typing import Any, Dict

import awsgi

from app import app
from utils import get_module_logger

LOGGER = get_module_logger(__name__)

"""
Example usage:
    >>> handler({"httpMethod": "GET", "path": "/"}, {})
    {"statusCode": 200, "headers": {...}, "body": "..."}
"""


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda entry point for the Flask application.
    This function acts as a bridge between AWS Lambda and the Flask app
    using the `awsgi.response` function to handle API Gateway events.
    :param event: The API Gateway event dictionary.
    :param context: The Lambda context object, which contains runtime info.
    :return: A response dictionary formatted for API Gateway.
    """
    try:
        return awsgi.response(app, event, context)

    except Exception as exc:
        # logger.exception captures stack trace in CloudWatch.
        LOGGER.exception("Unhandled exception in Lambda handler.")

        # Return a JSON-formatted 500 error for API Gateway
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "error": "Internal Server Error",
                    "message": (
                        str(exc)
                        if app.debug
                        else "An unexpected error occurred."
                    ),
                }
            ),
        }
