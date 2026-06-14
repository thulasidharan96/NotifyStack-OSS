# NotifyStack-OSS

## Backend

Run locally:

```bash
uv sync --all-groups
uv run uvicorn app.main:app --app-dir backend --reload
```

Test:

```bash
uv run pytest backend/tests
```
