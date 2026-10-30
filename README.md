# cyberforums-sdk

Cyberforums Python **reference** SDK. Calls **BFF open API only**.

**Not published** to PyPI yet.

## Usage (stub)

```python
from cyberforums_sdk import Client

client = Client(
    base_url="https://chat.example.com",
    token="...",  # from env in real use
)

client.get("/v1/healthz")
client.post("/v1/example", {"hello": "world"})
```

Docs: https://feicode.com/Cyberforums/cyberforums-docs

## Actor rules

Do not send `actor` / `actor_id` — server derives them from the token.
