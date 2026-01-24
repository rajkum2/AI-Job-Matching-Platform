# JobMatch MVP

Phase 1 MVP for an admin-only job matching platform with FastAPI, MongoDB, Qdrant, and a Next.js dashboard.

## Local Run

1) Copy env file:

```bash
cp .env.example .env
```

2) Start the stack:

```bash
docker-compose up --build
```

3) Open the dashboard:

- Dashboard: http://localhost:3000
- API: http://localhost:8000/health

Login with the `ADMIN_PASSWORD` from `.env`.

## Seed + Pipeline

Use the Overview page quick actions or call API endpoints:

- `POST /admin/seed`
- `POST /admin/normalize/all`
- `POST /admin/embed/jobs`
- `POST /admin/match/all`

## Embeddings

Default is deterministic hashing embeddings. To enable sentence-transformers:

- Install `sentence-transformers` in the API image
- Set `EMBED_USE_SENTENCE_TRANSFORMERS=true`

## Coolify

- Deploy using `docker-compose.yml`
- Expose ports 3000 (dashboard) and 8000 (API)
- Provide the `.env` values in Coolify environment variables

## Project Structure

- `api/` FastAPI backend
- `dashboard/` Next.js admin dashboard
- `docker-compose.yml` stack with MongoDB + Qdrant
- `api/seeds/` demo seed data
