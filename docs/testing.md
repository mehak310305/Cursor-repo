# Testing

```bash
source .venv/bin/activate
pytest
```

## Coverage areas

| Area | Tests |
|------|--------|
| Auth | Login success/failure, logout, anonymous redirects |
| Servers | Add success, duplicate host rejection, invalid host, auth gate |
| Metrics | Mock payload shape/ranges, allowlisted process names |
| APIs / UI | Dashboard JSON, detail JSON 404, detail page after add, anonymous denied |

Tests use a dedicated password hash from `tests/conftest.py` — never production secrets.
