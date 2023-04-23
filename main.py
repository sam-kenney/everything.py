"""Run the default Jade app."""
from __future__ import annotations

import flask
from gpt3 import GPT3Client
import typing


class App:
    """App class that preserves the Flask app and GPT-3 client."""

    def __init__(self, app: flask.Flask) -> None:
        """
        Create a new App instance.

        Params
        ------
        app: :class:`flask.Flask`
            The Flask app to use.
        """
        self.app = app
        self._gpt = GPT3Client()

    def __enter__(self) -> App:
        """Enter the context manager."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        self.close()

    def connect(self) -> None:
        """Connect to the GPT-3 API."""
        self._gpt.connect()

    def close(self) -> None:
        """Disconnect from the GPT-3 API."""
        self._gpt.close()

    @property
    def run(self) -> typing.Callable[..., None]:
        """Return the Flask app's run method."""
        return self.app.run

    @staticmethod
    def index() -> str:
        """Render the index page."""
        with open("templates/include/search.html", "r") as file:
            content = file.read()

        return flask.render_template("index.html", title="Home", content=content)

    def search(self) -> str:
        """Render the search page."""
        query = flask.request.args.get("q")
        body = self._gpt.query(
            f"""
            Create a web page in HTML format (starting from the <body> tag) that
            contains information relating to the following query: {query}
            This information should include links to relevant web pages, and
            other relevant information.
            """,
            timeout=200,
        )
        print(body)

        return flask.render_template("index.html", title=query, content=body)

    def register(self) -> None:
        """Register the routes."""
        self.app.add_url_rule("/", view_func=self.index)
        self.app.add_url_rule("/search", view_func=self.search)


if __name__ == "__main__":
    with App(flask.Flask(__name__)) as app:
        app.register()

        app.run(
            host="0.0.0.0",
            port=8080,
            debug=True,
        )
