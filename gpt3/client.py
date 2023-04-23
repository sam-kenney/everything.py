"""Module to interface with the GPT-3 API."""
from __future__ import annotations

import os

import httpx
import typing_extensions as tx


class GPT3Client:
    """Interface with the GPT-3 API."""

    def __init__(self, token: str | None = None) -> None:
        """Interface with the GPT-3 API."""
        self.token = os.environ.get("OPENAI_API_TOKEN", token)

        self._client: httpx.Client

        if not self.token:
            raise ValueError(
                "No API token provided. "
                + "Please set the `OPENAI_API_TOKEN`"
                + "environment variable, or pass "
                + "it to the constructor explicitly",
            )

    def __enter__(self: tx.Self) -> GPT3Client:
        """Open the Client as a context manager."""
        self.connect()
        return self

    def __exit__(self: tx.Self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        self.close()

    def connect(self: tx.Self) -> None:
        """Connect to the HTTP async client."""
        self._client = httpx.Client(
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            }
        )

    def close(self: tx.Self) -> None:
        """Close the client."""
        self._client.close()

    def query(self: tx.Self, question: str, **kwargs) -> str:
        """Ask a question to Chat GPT."""
        response = self._client.post(
            "https://api.openai.com/v1/chat/completions",
            json={
                "messages": [{"role": "user", "content": question}],
                "model": "gpt-3.5-turbo",
            },
            **kwargs,
        )

        if response.status_code != 200:
            response.raise_for_status()

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        raise httpx.HTTPError("Something went wrong :(")
