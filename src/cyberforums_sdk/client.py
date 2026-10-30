from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Mapping, Optional


class Client:
    """Thin BFF HTTP client stub."""

    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    def get(self, path: str, headers: Optional[Mapping[str, str]] = None) -> Any:
        return self._request("GET", path, body=None, headers=headers)

    def post(
        self,
        path: str,
        body: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        return self._request("POST", path, body=body, headers=headers)

    def _request(
        self,
        method: str,
        path: str,
        body: Optional[Any],
        headers: Optional[Mapping[str, str]],
    ) -> Any:
        url = f"{self.base_url}{path if path.startswith('/') else '/' + path}"
        data = None if body is None else json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {self.token}")
        if body is not None:
            req.add_header("Content-Type", "application/json")
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read()
                if not raw:
                    return None
                ctype = resp.headers.get("Content-Type", "")
                if "application/json" in ctype:
                    return json.loads(raw.decode("utf-8"))
                return raw.decode("utf-8")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code}: {detail}") from e
