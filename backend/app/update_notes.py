"""Run from inside the backend container: python -m app.update_notes"""
import os
from app.database import SessionLocal
from app.models import Topic, Note

DOCS_DIR = os.path.join(os.path.dirname(__file__), "data", "docs")

db = SessionLocal()
updated = 0
added = 0

for fname in os.listdir(DOCS_DIR):
    if not fname.endswith(".md"):
        continue
    slug = fname[:-3]
    topic = db.query(Topic).filter(Topic.slug == slug).first()
    if not topic:
        print(f"SKIP (no topic): {slug}")
        continue
    with open(os.path.join(DOCS_DIR, fname)) as f:
        content = f.read()
    note = db.query(Note).filter(Note.topic_id == topic.id, Note.is_prebuilt == True).first()
    if note:
        note.content = content
        updated += 1
    else:
        db.add(Note(topic_id=topic.id, content=content, is_prebuilt=True))
        added += 1

db.commit()
db.close()
print(f"Done. Updated: {updated}, Added: {added}")
