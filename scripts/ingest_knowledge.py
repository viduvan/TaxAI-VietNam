"""
Knowledge Base Ingestion Script.
Reads 12 MD reference files → chunks by ## section → embeds → inserts into pgvector.

Usage:
    python scripts/ingest_knowledge.py

Requires Ollama running with nomic-embed-text model.
"""

import os
import re
import httpx
import psycopg2
from psycopg2.extras import execute_values

# Configuration
REFERENCES_DIR = os.getenv("REFERENCES_DIR", "./references")
SKILL_FILE = os.getenv("SKILL_FILE", "./SKILL.md")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://taxai:taxai_secure_2026@localhost:5432/taxai"
)

# Confidence mapping per file
CONFIDENCE_MAP = {
    "tong-quan-thue.md": "HIGH",
    "sop-quyet-toan.md": "HIGH",
    "freelancer-guide.md": "HIGH",
    "deadline-tracker.md": "HIGH",
    "thue-khoan-guide.md": "HIGH",
    "changelog.md": "HIGH",
    "sources.md": "HIGH",
    "nguoi-nuoc-ngoai-guide.md": "HIGH",
    "bhxh-rut-mot-lan-guide.md": "HIGH",
    "bhtn-tro-cap-guide.md": "HIGH",
    "vi-du-tinh-thue.md": "MEDIUM",
    "faq.md": "MEDIUM",
}


def chunk_markdown(text: str, source_file: str) -> list[dict]:
    """
    Split markdown into chunks by ## headings.
    Each chunk = one section with its heading.
    """
    chunks = []
    sections = re.split(r'^(#{1,3}\s+.+)$', text, flags=re.MULTILINE)

    current_title = source_file
    current_text = ""

    for part in sections:
        part = part.strip()
        if not part:
            continue

        if re.match(r'^#{1,3}\s+', part):
            # Save previous chunk
            if current_text.strip():
                chunks.append({
                    "source_file": source_file,
                    "section_title": current_title,
                    "chunk_text": current_text.strip(),
                    "confidence": CONFIDENCE_MAP.get(source_file, "MEDIUM"),
                })
            current_title = part.lstrip('#').strip()
            current_text = ""
        else:
            current_text += part + "\n"

    # Save last chunk
    if current_text.strip():
        chunks.append({
            "source_file": source_file,
            "section_title": current_title,
            "chunk_text": current_text.strip(),
            "confidence": CONFIDENCE_MAP.get(source_file, "MEDIUM"),
        })

    return chunks


def get_embedding(text: str) -> list[float]:
    """Get embedding from Ollama nomic-embed-text model."""
    response = httpx.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text[:8000]},
        timeout=60.0,
    )
    response.raise_for_status()
    return response.json()["embedding"]


def extract_law_reference(text: str) -> str | None:
    """Extract law references from chunk text."""
    patterns = [
        r'Luật\s+\d+/\d+/QH\d+',
        r'NĐ\s+\d+/\d+/NĐ-CP',
        r'NQ\s+\d+/\d+/\w+',
        r'TT\s+\d+/\d+/TT-BTC',
    ]
    refs = []
    for p in patterns:
        matches = re.findall(p, text)
        refs.extend(matches)

    return ", ".join(refs[:3]) if refs else None


def main():
    print("═" * 50)
    print("TaxAI Knowledge Base Ingestion")
    print("═" * 50)

    # Collect all MD files
    all_chunks = []

    # Process reference files
    for filename in sorted(os.listdir(REFERENCES_DIR)):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(REFERENCES_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_markdown(text, filename)
        all_chunks.extend(chunks)
        print(f"  📄 {filename}: {len(chunks)} chunks")

    # Process SKILL.md
    if os.path.exists(SKILL_FILE):
        with open(SKILL_FILE, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_markdown(text, "SKILL.md")
        all_chunks.extend(chunks)
        print(f"  📄 SKILL.md: {len(chunks)} chunks")

    print(f"\n  Total chunks: {len(all_chunks)}")
    print(f"\n🔄 Generating embeddings...")

    # Generate embeddings
    for i, chunk in enumerate(all_chunks):
        chunk["embedding"] = get_embedding(chunk["chunk_text"])
        chunk["law_reference"] = extract_law_reference(chunk["chunk_text"])

        if (i + 1) % 10 == 0:
            print(f"  Embedded {i + 1}/{len(all_chunks)}")

    print(f"  ✅ All {len(all_chunks)} embeddings generated")

    # Insert into PostgreSQL
    print(f"\n💾 Inserting into PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Clear existing data
    cur.execute("DELETE FROM knowledge_chunks")

    # Insert chunks
    values = [
        (
            c["source_file"],
            c["section_title"],
            c["chunk_text"],
            str(c["embedding"]),
            c["confidence"],
            c["law_reference"],
        )
        for c in all_chunks
    ]

    execute_values(
        cur,
        """INSERT INTO knowledge_chunks 
           (source_file, section_title, chunk_text, embedding, confidence, law_reference)
           VALUES %s""",
        values,
    )

    # Create ivfflat index (needs data first)
    cur.execute("DROP INDEX IF EXISTS idx_chunks_embedding_ivfflat")
    cur.execute(
        """CREATE INDEX idx_chunks_embedding_ivfflat 
           ON knowledge_chunks USING ivfflat (embedding vector_cosine_ops)
           WITH (lists = 10)"""
    )

    conn.commit()
    cur.close()
    conn.close()

    print(f"  ✅ Inserted {len(all_chunks)} chunks into knowledge_chunks")
    print(f"\n{'═' * 50}")
    print("✅ Ingestion complete!")


if __name__ == "__main__":
    main()
