# DecodeLabs Task API (Python) — Project 2: Backend API Development

A simple REST API built with Python + Flask, covering the required skills:
API endpoints (GET/POST), handling user input, and basic data validation.

This is a Python port of the same API — same endpoints, same validation
rules, same status codes.

## Setup

```bash
pip install -r requirements.txt
python3 server.py
```

Server runs at `http://localhost:3000`.

## Endpoints

| Method | Path         | Description                          | Success | Error cases                  |
|--------|--------------|---------------------------------------|---------|-------------------------------|
| GET    | `/`          | API info / health check               | 200     | —                              |
| GET    | `/tasks`     | List all tasks                        | 200     | —                              |
| GET    | `/tasks/:id` | Get one task by id                    | 200     | 400 (bad id), 404 (not found)  |
| POST   | `/tasks`     | Create a new task                     | 201     | 400 (invalid/missing fields)   |

### POST /tasks — request body

```json
{
  "title": "Buy groceries",
  "completed": false
}
```

- `title` (string, required, 1–100 characters after trimming)
- `completed` (boolean, optional, defaults to `false`)

### Example requests

```bash
curl http://localhost:3000/tasks

curl -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Ship the feature"}'
```

## Project structure

```
task-api-py/
├── server.py              # App entry point, error handlers
├── requirements.txt
├── routes/
│   └── tasks.py            # Blueprint: GET /tasks, GET /tasks/:id, POST /tasks
├── middleware/
│   └── validate.py         # "Gatekeeper Rule" — syntactic + semantic validation
└── data/
    └── store.py             # In-memory data store (stand-in for a real DB)
```

## Design notes (mapped to the training slides)

- **RESTful naming** — resources are nouns (`/tasks`), actions come from the
  HTTP method, not the URL (no `/get_tasks` or `/create_task`).
- **The Gatekeeper Rule** (`middleware/validate.py`) — every POST body is
  checked syntactically (right types present) and semantically (non-empty,
  reasonable length) before touching the data layer.
- **Status codes** — `200` for reads, `201` for created resources, `400` for
  bad client input, `404` for missing resources/routes, `500` as a safety
  net for unexpected server errors.
- **Statelessness** — each request carries everything needed to process it;
  the server keeps no per-client session between requests.

## Possible extensions

- Add `PUT /tasks/<id>` and `DELETE /tasks/<id>` to complete full CRUD.
- Swap the in-memory `data/store.py` for a real database (SQLite/Postgres).
- Add authentication (AuthN) and authorization (AuthZ) via a decorator.
- Add rate limiting (e.g. Flask-Limiter) to return `429 Too Many Requests`.
- Run with a production WSGI server (gunicorn) instead of the Flask dev server.
