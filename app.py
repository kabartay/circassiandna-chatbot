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
import os
from typing import Any, Dict, List, Optional, Union

from flask import Flask, jsonify, render_template, request
from openai import OpenAI, OpenAIError
from pinecone import Pinecone  # ServerlessSpec
from pinecone.exceptions import PineconeException

from utils import get_module_logger

LOGGER = get_module_logger(__name__)

# -------------------
# Environment
# -------------------
OPENAI_API_KEY: Optional[str] = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY: Optional[str] = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX: str = os.environ.get(
    "PINECONE_INDEX", "circassiandna-knowledgebase"
)
PINECONE_ENVIRONMENT: Optional[str] = os.environ.get("PINECONE_ENVIRONMENT")
PINECONE_CLOUD: Optional[str] = os.environ.get("PINECONE_CLOUD")
PINECONE_REGION: Optional[str] = os.environ.get("PINECONE_REGION")
PINECONE_NAMESPACE: Optional[str] = os.environ.get("PINECONE_NAMESPACE")

# -------------------
# Config
# -------------------
MODEL = "gpt-4o-mini"
TOP_N = 3  # for model
BATCH_SIZE = 50  # for indexes
PORT = 8080


if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is required")

client = OpenAI(api_key=OPENAI_API_KEY)


# -------------------
# Load Knowledge Base
# -------------------
try:
    with open("knowledgebase.json", "r", encoding="utf-8") as f:
        KNOWLEDGEBASE: Dict[str, str] = json.load(f)
except (OSError, json.JSONDecodeError) as err:
    raise RuntimeError(f"Failed to load knowledgebase.json: {err}") from err


# -------------------
# Embedding
# -------------------
def embed_text(text: str) -> List[float]:
    """
    Generate an embedding using OpenAI.
    Uses the `text-embedding-3-small` embedding model.
    The dimension (1536) matches the Pinecone index configuration.
    :param text: The input text to be converted into a vector representation.
    :return: A 1536-dim embedding vector corresponding to the input text.
    """
    try:
        model = "text-embedding-3-small"
        response = client.embeddings.create(model=model, input=text)
        return response.data[0].embedding
    except OpenAIError as err:
        LOGGER.error(
            "Embedding generation failed for text='%s': %s", text, err
        )
        raise
    except Exception:
        LOGGER.exception("Unexpected error during embedding generation.")
        raise


# -------------------
# Build indexes
# -------------------
def build_index(pc, index_name: str = PINECONE_INDEX) -> None:
    """
    Build or rebuild the Pinecone index with knowledgebase data.
    This function checks if the specified Pinecone index exists and creates it
    if necessary. It then embeds each entry from the knowledge base using
    OpenAI's embedding API and uploads the vectors to Pinecone in batches.
    :param pc: An initialized Pinecone client instance.
    :param index_name: Name of the index to create or update.
    :return: None.
    """
    try:
        indexes = pc.list_indexes().names()
        LOGGER.info("Current Pinecone indexes: %s", indexes)

        if index_name not in indexes:
            if not PINECONE_CLOUD or not PINECONE_REGION:
                raise RuntimeError(
                    "PINECONE_CLOUD and PINECONE_REGION are not found."
                )
            pc.create_index(
                name=index_name,
                dimension=1536,  # matches text-embedding-3-small
                metric="cosine",
                # spec=ServerlessSpec(
                #     cloud=PINECONE_CLOUD, region=PINECONE_REGION
                # ),
            )
            LOGGER.info("Created new Pinecone index: %s", index_name)

        idx = pc.Index(index_name)
        LOGGER.info("Indexes stats: %s", idx.describe_index_stats())

        vectors = []
        for i, (k, v) in enumerate(KNOWLEDGEBASE.items()):
            try:
                text = f"{k}\n{v}"
                emb = embed_text(text)
                vectors.append((str(i), emb, {"title": k, "text": v}))
            except OpenAIError:
                LOGGER.warning("Skipping entry %r due to embedding failure", k)
                continue

        for i in range(0, len(vectors), BATCH_SIZE):
            batch = vectors[i : i + BATCH_SIZE]
            LOGGER.info(
                "Uploading batch %s to %s: (%s vectors)",
                i,
                i + len(batch),
                len(batch),
            )
            # LOGGER.info(
            #     "Uploading batch %s to %s (%s vectors)",
            #     i,
            #     i + len(batch) - 1,
            #     len(batch),
            # )
            idx.upsert(vectors=batch)
            LOGGER.debug("Uploaded batch %d-%d", i, i + len(batch))

        LOGGER.info("Index build complete with %d vectors.", len(vectors))
    except PineconeException:
        LOGGER.exception("Pinecone operation failed during index build.")
        raise
    except Exception:
        LOGGER.exception("Unexpected error while building Pinecone index.")
        raise


# -------------------
# Query
# -------------------
def query_index(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Query Pinecone index, fallback to knowledge base if unavailable.
    :param query: Search query.
    :param top_k: Max number of results.
    :return: List of matched documents with
        - entry title;
        - entry text;
        - similarity score (1.0 for keyword matches).
    """
    if top_k < 1:
        raise ValueError("top_k must be >= 1")

    def _fallback_search() -> List[Dict[str, Union[str, float]]]:
        """
        Perform a simple keyword search over the local knowledge base.
        This function searches both the keys (titles) and values (content)
        of the knowledge base dictionary for the given query string.
        Matching entries are returned with a fixed score of 1.0.
        :return: A list of matching entries.
        """
        results = []
        for k, v in KNOWLEDGEBASE.items():
            if query.lower() in k.lower() or query.lower() in v.lower():
                results.append({"title": k, "text": v, "score": 1.0})
        return results[:top_k]

    try:
        if not PINECONE_API_KEY:
            LOGGER.warning("PINECONE_API_KEY not set.")
            LOGGER.warning("Using fallback KB search.")
            return _fallback_search()

        # Initialize Pinecone client
        pc = Pinecone(
            api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT
        )

        if PINECONE_INDEX not in pc.list_indexes().names():
            LOGGER.warning("Pinecone index not found: %s.", PINECONE_INDEX)
            LOGGER.warning("Using fallback KB search.")
            return _fallback_search()

        idx = pc.Index(PINECONE_INDEX)
        try:
            q_emb = embed_text(query)
        except OpenAIError as err:
            LOGGER.error("OpenAI embedding generation failed: %s", err)
            return _fallback_search()

        # Query Pinecone API
        results = idx.query(
            vector=q_emb,
            top_k=top_k,
            namespace=PINECONE_NAMESPACE,
            include_metadata=True,
        )

        # Extract matches
        # Access matches correctly from the QueryResponse object
        # Uses match.metadata.get() so missing keys won’t cause crashes.
        data = [
            {
                "title": match.metadata.get("title"),
                "text": match.metadata.get("text"),
                "score": match.score,
            }
            for match in results.matches
        ]

        return data
    except PineconeException as err:
        LOGGER.error("Pinecone query failed: %s", err)
        return _fallback_search()

    except Exception as err:
        LOGGER.exception("Unexpected error during query_index(): %s", err)
        return _fallback_search()


# -------------------
# Flask App
# -------------------
app = Flask(__name__)


def retrieve_context(
    question: str, top_n: int = TOP_N
) -> List[Dict[str, Any]]:
    """
    Retrieve the most relevant knowledge base entries for a given question.
    :param question: The user's input question.
    :param top_n: Maximum number of relevant entries to return.
    :return: A list of dictionaries, each containing
        (q) The question/title from the knowledge base.
        (a) The corresponding answer/text.
        (score) Relevance score from Pinecone, if available.
    """
    try:
        hits = query_index(question, top_k=top_n)
        return [
            {"q": h["title"], "a": h["text"], "score": h.get("score")}
            for h in hits
        ]
    except PineconeException as err:
        LOGGER.exception("Pinecone query failed. %s", err)
        return []
    except Exception as err:
        LOGGER.exception("Unexpected error during context retrieval. %s", err)
        return []


@app.route("/")
def index() -> str:
    """
    Render the main chatbot UI page.
    :return: Rendered HTML for the chatbot interface.
    """
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Handle chat requests from the client.

    This endpoint:
      - Receives a JSON payload with a "question" field.
      - Retrieves relevant context from Pinecone or a fallback knowledge base.
      - Constructs a prompt for the OpenAI model.
      - Returns the model's answer as JSON.

    Request JSON:
        {
            "question": "<user's question>"
        }

    Response JSON:
        {
            "answer": "<generated answer>"
        }
    :return: Flask response as JSON with generated answer or an error msg.
    """

    def error_response(message: str, status_code: int):
        """Helper to format error responses consistently."""
        return {"error": message}, status_code

    response_data = None
    status_code = 200

    try:
        data = request.json or {}
    except Exception as err:
        LOGGER.exception("Invalid JSON in request. %s", err)
        response_data, status_code = error_response(
            "Invalid JSON payload", 400
        )
    else:
        question = data.get("question")
        if not question:
            response_data, status_code = error_response(
                "No question provided", 400
            )
        else:
            try:
                contexts = retrieve_context(question)
            except PineconeException as err:
                LOGGER.exception("Pinecone query failed.")
                response_data, status_code = error_response(
                    f"Pinecone error: {str(err)}", 500
                )
            except Exception as err:
                LOGGER.exception("Unexpected error during context retrieval.")
                response_data, status_code = error_response(
                    f"Context retrieval error: {str(err)}", 500
                )
            else:
                LOGGER.info("Pinecone results: %s", contexts)
                combined_context = "\n\n".join(
                    f"Q: {c['q']}\nA: {c['a']}" for c in contexts
                )

                prompt = (
                    "You are a helpful assistant for Circassian DNA.\n"
                    "Use knowledge base entries to answer the question.\n\n"
                    f"Knowledge base: {combined_context}\n\n"
                    f"Question: {question}\n"
                    "Answer:"
                )

                try:
                    completion = client.chat.completions.create(
                        model=MODEL,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    answer = completion.choices[0].message.content
                except OpenAIError as err:
                    LOGGER.exception("OpenAI API request failed.")
                    response_data, status_code = error_response(
                        f"OpenAI API error: {str(err)}", 500
                    )
                except Exception as err:
                    LOGGER.exception("Unexpected error during OpenAI request.")
                    response_data, status_code = error_response(
                        f"Answer generation error: {str(err)}", 500
                    )
                else:
                    response_data = {"answer": answer}

    return jsonify(response_data), status_code


# -------------------
# Entrypoint
# -------------------
if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "build":
        if not PINECONE_API_KEY:
            raise RuntimeError("PINECONE_API_KEY is required for index build.")
        pc = Pinecone(api_key=PINECONE_API_KEY)
        build_index(pc)
    else:
        port = int(os.environ.get("PORT", PORT))
        app.run(host="0.0.0.0", port=port)
