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

from unittest.mock import MagicMock, patch

import pytest
from openai import OpenAIError

from app import (
    KNOWLEDGEBASE,
    app,
    build_index,
    embed_text,
    query_index,
    retrieve_context,
)


@pytest.fixture
def flask_client():
    """Flask test client fixture."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestEmbedText:
    """
    Tests for the `embed_text` function which generates embedding vectors
    from input text using OpenAI's embedding API.

    Verifies:
    - Successful embedding returns the expected vector.
    - Exceptions from OpenAI API are properly propagated.
    """

    @patch("app.client.embeddings.create")
    def test_embed_text_success(self, create):
        """Embed_text should return the embedding vector on success."""
        create.return_value = MagicMock(
            data=[MagicMock(embedding=[0.1, 0.2, 0.3])]
        )
        emb = embed_text("hello")
        assert emb == [0.1, 0.2, 0.3]
        create.assert_called_once()

    @patch("app.client.embeddings.create")
    def test_embed_text_openai_error(self, create):
        """Embed_text should propagate OpenAIError exceptions."""
        create.side_effect = OpenAIError("API failure")
        with pytest.raises(OpenAIError):
            embed_text("fail")


class TestBuildIndex:
    """
    Tests for the `build_index` function which constructs or updates a Pinecone
    index with embedded knowledge base data.

    Verifies:
    - Creation of the Pinecone index if it does not exist.
    - Calling of `upsert` to upload embedding vectors in batches.
    - Embeddings are generated for knowledge base entries.
    """

    @patch("app.BATCH_SIZE", 2)
    @patch("app.embed_text")
    @patch("app.Pinecone")
    def test_build_index_creates_and_upserts(self, pc_cls, mock_embed_text):
        """
        Test that build_index:
        - calls Pinecone's create_index when the index does not exist,
        - calls upsert on the Pinecone index to upload vectors,
        - calls embed_text to generate embeddings.
        """

        index_name = "test_index"
        dimension = 1536

        # Embedding output
        mock_embed_text.return_value = [0.0] * dimension

        # Setup Pinecone instance
        pc_instance = pc_cls.return_value

        # Make list_indexes().names() return empty list so index is created
        list_indexes_result = MagicMock()
        list_indexes_result.names.return_value = []
        pc_instance.list_indexes.return_value = list_indexes_result
        pc_instance.create_index.return_value = None

        # Make create_index to track calls
        pc_instance.create_index = MagicMock()

        # Make index returned by pc_instance.Index()
        index = MagicMock()
        pc_instance.Index.return_value = index

        # Clear and populate knowledge base
        KNOWLEDGEBASE.clear()
        KNOWLEDGEBASE["key1"] = "value1"

        build_index(pc_instance, index_name=index_name)

        pc_instance.create_index.assert_called_once_with(
            name=index_name, dimension=dimension, metric="cosine"
        )
        assert (
            index.upsert.call_count > 0
        ), "Expected upsert to be called at least once"
        assert index.upsert.called
        assert mock_embed_text.called


class TestQueryIndex:
    """
    Tests for the `query_index` function that queries the knowledge base.

    Verifies:
    - Proper fallback to simple search when Pinecone API key is missing.
    - Querying Pinecone index returns relevant search results with scores.
    """

    def test_query_index_fallback_search(self, monkeypatch):
        """
        Query_index falls back to simple search
        when Pinecone API key is missing.
        """
        monkeypatch.setattr("app.PINECONE_API_KEY", None)
        monkeypatch.setattr(
            "app.KNOWLEDGEBASE", {"hello": "world", "foo": "bar"}
        )

        results = query_index("hello")
        assert isinstance(results, list)
        assert any(
            "hello" in r["title"].lower() or "hello" in r["text"].lower()
            for r in results
        )
        assert all("score" in r for r in results)

    @patch("app.Pinecone")
    @patch("app.embed_text")
    def test_query_index_with_pinecone(
        self, mock_embed_text, pc_cls, monkeypatch
    ):
        """Query_index queries Pinecone index when API key is set."""
        monkeypatch.setattr("app.PINECONE_API_KEY", "fake_key")

        pc_instance = pc_cls.return_value
        # Make list_indexes to return object with .names() method return list
        pc_instance.list_indexes.return_value = MagicMock(
            names=lambda: ["circassiandna-knowledgebase"]
        )
        index = MagicMock()
        pc_instance.Index.return_value = index

        mock_embed_text.return_value = [0.1] * 1536

        # Simulate query result matches
        class Match:
            """A simple container class representing a search result match."""

            def __init__(self, title, text, score):
                self.metadata = {"title": title, "text": text}
                self.score = score

        index.query.return_value = MagicMock(
            matches=[
                Match("Title1", "Text1", 0.99),
                Match("Title2", "Text2", 0.85),
            ]
        )

        results = query_index("query")

        assert len(results) == 2
        assert results[0]["title"] == "Title1"
        assert results[0]["score"] == 0.99


class TestRetrieveContext:
    """
    Tests for the `retrieve_context` function which formats query results
    for downstream use.

    Verifies:
    - The returned context contains the expected fields and matches
      the query_index results.
    """

    @patch("app.query_index")
    def test_retrieve_context(self, mock_query_index):
        """
        Retrieve_context should format the query_index results correctly.
        """
        mock_query_index.return_value = [
            {"title": "Q1", "text": "A1", "score": 0.9},
            {"title": "Q2", "text": "A2", "score": 0.8},
        ]

        results = retrieve_context("some question")

        assert len(results) == 2
        for item in results:
            assert "q" in item and "a" in item and "score" in item

        assert results[0]["q"] == "Q1"
        assert results[0]["a"] == "A1"


class TestFlaskEndpoints:
    """
    Tests for the Flask web application endpoints.

    Verifies:
    - The index route returns an HTML page.
    - The chat API route returns answers for valid questions.
    - The chat API route returns appropriate errors for missing/nvalid input.
    """

    def test_index_route(self, flask_client):
        """GET / should return HTML page."""
        resp = flask_client.get("/")
        assert resp.status_code == 200
        assert b"<!DOCTYPE html>" in resp.data or b"<html" in resp.data

    @patch("app.retrieve_context")
    @patch("app.client.chat.completions.create")
    def test_chat_route_success(
        self, completion_create, mock_retrieve_context, flask_client
    ):
        """POST /api/chat returns an answer when question is provided."""
        mock_retrieve_context.return_value = [
            {"q": "Q", "a": "A", "score": 1.0}
        ]
        completion_create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test answer"))]
        )

        resp = flask_client.post(
            "/api/chat", json={"question": "What is DNA?"}
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert "answer" in data
        assert data["answer"] == "Test answer"

    def test_chat_route_no_question(self, flask_client):
        """POST /api/chat with no question returns 400."""
        resp = flask_client.post("/api/chat", json={})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data is not None
        assert "error" in data

    def test_chat_route_invalid_json(self, flask_client):
        """POST /api/chat with invalid JSON returns 400."""
        resp = flask_client.post(
            "/api/chat", data="invalid json", content_type="application/json"
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert data is not None
        assert "error" in data
