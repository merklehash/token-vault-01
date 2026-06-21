# API Token Manager

A CLI tool to manage your API tokens with JSON-based storage.

## Features

- **Create** — add a new API token with service name, value, and billing amount
- **Read** — list all tokens or search by service name
- **Update** — edit name, token value, status, or billing
- **Delete** — remove a token by ID
- **Stats** — overview of active/inactive tokens and total billing

## Usage

```bash
python token_manager.py
```

No dependencies — standard library only (`json`, `os`, `uuid`, `datetime`).
> Yes, it's a JSON file.
