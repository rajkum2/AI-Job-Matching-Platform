# Coolify Deployment Notes

## Required Environment Variables

- `ADMIN_PASSWORD`
- `ADMIN_TOKEN_SECRET`
- `MONGODB_URI` (default in compose: `mongodb://mongo:27017`)
- `QDRANT_URL` (default in compose: `http://qdrant:6333`)
- `API_BASE_URL` (public URL the dashboard uses to reach the API)
- `EMBED_USE_SENTENCE_TRANSFORMERS` (optional, default false)

## Domains

- Attach your public domain to the `dashboard` service.
- If API is exposed publicly, set `API_BASE_URL` to that public API URL.

## Internal Service URLs

- API to MongoDB: `mongodb://mongo:27017`
- API to Qdrant: `http://qdrant:6333`

## Volumes

- `mongo_data` for MongoDB persistence
- `qdrant_data` for Qdrant persistence
