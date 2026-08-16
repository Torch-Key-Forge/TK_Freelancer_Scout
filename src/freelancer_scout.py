"""Minimal read-only Freelancer project search client.

This public example intentionally exposes no mutation methods.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


PRODUCTION_API = "https://www.freelancer.com/api"
SANDBOX_API = "https://www.freelancer-sandbox.com/api"
ALLOWED_API_BASES = frozenset({PRODUCTION_API, SANDBOX_API})
ACTIVE_PROJECTS_PATH = "/projects/0.1/projects/active/"
TOKEN_ENVIRONMENT_VARIABLE = "FLN_OAUTH_TOKEN"


class ScoutError(RuntimeError):
    """Raised when the bounded read-only request cannot be completed."""


@dataclass(frozen=True)
class ScoutConfig:
    token: str
    api_base: str = PRODUCTION_API
    timeout_seconds: float = 20.0

    def __post_init__(self) -> None:
        if not self.token.strip():
            raise ValueError("A non-empty OAuth token is required.")
        if self.api_base not in ALLOWED_API_BASES:
            raise ValueError("api_base must be the Freelancer production or sandbox API.")
        if not 1 <= self.timeout_seconds <= 60:
            raise ValueError("timeout_seconds must be between 1 and 60.")


class FreelancerScout:
    """GET-only client for active-project discovery."""

    def __init__(
        self,
        config: ScoutConfig,
        *,
        opener: Callable[..., Any] = urlopen,
    ) -> None:
        self._config = config
        self._opener = opener

    def search_active_projects(self, query: str, *, limit: int = 10) -> dict[str, Any]:
        clean_query = query.strip()
        if not clean_query:
            raise ValueError("query must not be empty.")
        if not 1 <= limit <= 20:
            raise ValueError("limit must be between 1 and 20.")

        parameters = urlencode(
            {
                "query": clean_query,
                "limit": limit,
                "offset": 0,
            }
        )
        return self._get_json(f"{ACTIVE_PROJECTS_PATH}?{parameters}")

    def _get_json(self, path_and_query: str) -> dict[str, Any]:
        request = Request(
            f"{self._config.api_base}{path_and_query}",
            headers={
                "Accept": "application/json",
                "Freelancer-OAuth-V1": self._config.token,
                "User-Agent": "Torch-Key-Freelancer-Scout/0.1",
            },
            method="GET",
        )

        try:
            with self._opener(request, timeout=self._config.timeout_seconds) as response:
                payload = response.read().decode("utf-8")
        except HTTPError as exc:
            raise ScoutError(f"Freelancer returned HTTP {exc.code}.") from exc
        except URLError as exc:
            raise ScoutError("The Freelancer API could not be reached.") from exc

        try:
            decoded = json.loads(payload)
        except json.JSONDecodeError as exc:
            raise ScoutError("Freelancer returned a non-JSON response.") from exc
        if not isinstance(decoded, dict):
            raise ScoutError("Freelancer returned an unexpected response shape.")
        return decoded


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search Freelancer active projects without taking marketplace actions."
    )
    parser.add_argument("--query", required=True, help="Opportunity search text.")
    parser.add_argument("--limit", type=int, default=10, help="Result limit, from 1 to 20.")
    parser.add_argument(
        "--sandbox",
        action="store_true",
        help="Use the Freelancer sandbox API.",
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    token = os.environ.get(TOKEN_ENVIRONMENT_VARIABLE, "")
    if not token:
        raise SystemExit(
            f"Set {TOKEN_ENVIRONMENT_VARIABLE} in the local process environment."
        )

    config = ScoutConfig(
        token=token,
        api_base=SANDBOX_API if args.sandbox else PRODUCTION_API,
    )
    scout = FreelancerScout(config)
    result = scout.search_active_projects(args.query, limit=args.limit)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

