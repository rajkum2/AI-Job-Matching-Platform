from datetime import datetime
from typing import List, Optional

from app.db.mongo import get_db, serialize_docs


async def log_event(actor: str, action: str, entity_type: str, entity_id: str, before: Optional[dict], after: Optional[dict]) -> None:
    doc = {
        "actor": actor,
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "before": before,
        "after": after,
        "created_at": datetime.utcnow(),
    }
    await get_db().audit_events.insert_one(doc)


async def list_events() -> List[dict]:
    docs = await get_db().audit_events.find().sort("created_at", -1).to_list(50)
    return serialize_docs(docs)
