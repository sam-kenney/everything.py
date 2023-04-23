"""Module to interface with the GPT-3 API."""
from __future__ import annotations

import os

import httpx
import typing_extensions as tx


class GPT3AsyncClient:
    """Interface with the GPT-3 API."""

    def __init__(self, token: str | None = None) -> None:
        """Interface with the GPT-3 API."""
        self.token = os.environ.get("OPENAI_API_TOKEN", token)

        self._client: httpx.AsyncClient

        if not self.token:
            raise ValueError(
                "No API token provided. "
                + "Please set the `OPENAI_API_TOKEN`"
                + "environment variable, or pass "
                + "it to the constructor explicitly",
            )

    async def __aenter__(self: tx.Self) -> GPT3AsyncClient:
        """Open the Client as a context manager."""
        await self.connect()
        return self

    async def __aexit__(self: tx.Self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        await self.aclose()

    async def connect(self: tx.Self) -> None:
        """Connect to the HTTP async client."""
        self._client = httpx.AsyncClient(
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            }
        )

    async def aclose(self: tx.Self) -> None:
        """Close the client."""
        await self._client.aclose()

    async def query(self: tx.Self, question: str, **kwargs) -> str:
        """Ask a question to Chat GPT."""
        response = await self._client.post(
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
