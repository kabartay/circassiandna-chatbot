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

from apig_wsgi import make_lambda_handler

from app import app

# Create the AWS Lambda handler
# This produces a function with signature (event, context) -> dict
# Works for both API Gateway REST (v1) and HTTP API (v2) events.
handler = make_lambda_handler(app)

# Note: The above handler is a simplified version using apig_wsgi.
# Custom handler with awsgi2; TODO: debug

# import json
# from typing import Any, Dict, Mapping

# import awsgi2

# from app import app
# from utils import get_module_logger

# LOGGER = get_module_logger(__name__)


# def handler(event: Dict[str, Any], context: Any) -> Mapping[str, Any]:
#     """
#     AWS Lambda entry point for the Flask application.
#     This function acts as a bridge between AWS Lambda and the Flask app
#     using the `awsgi2.response` function to handle API Gateway events.
#     :param event: The API Gateway event dictionary.
#     :param context: The Lambda context object, which contains runtime info.
#     :return: A response dictionary formatted for API Gateway.
#     """
#     try:
#         LOGGER.info("Received event: %s", event)

#         # # Detect API Gateway version
#         # if "version" in event and event["version"] == "2.0":
#         #     is_v2 = True  # HTTP API
#         # elif "httpMethod" in event:
#         #     is_v2 = False  # REST API
#         # else:
#         #     raise ValueError("Unknown API Gateway event type")

#         # Let awsgi2 auto-detect API Gateway version
#         return awsgi2.response(app, event, context)

#     except Exception as exc:
#         # Exception captures stack trace in CloudWatch.
#         LOGGER.exception("Unhandled exception in Lambda handler.")

#         # Return a JSON-formatted 500 error for API Gateway
#         err_msg = "An unexpected error occurred."
#         return {
#             "statusCode": 500,
#             "headers": {"Content-Type": "application/json"},
#             "body": json.dumps(
#                 {
#                     "error": "Internal Server Error",
#                     "message": (
#                         str(exc) if app.debug else err_msg
#                     ),
#                 }
#             ),
#         }
