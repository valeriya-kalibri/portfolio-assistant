"""Chunk and embed the markdown files in kb/ into Supabase as seed documents.

Usage: python ingest.py
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from rag.documents import store_seed_document

KB_DIR = Path(__file__).resolve().parent.parent / "kb"


def main():
    for path in sorted(KB_DIR.glob("*.md")):
        print(f"Ingesting {path.name}...")
        count = store_seed_document(path.stem, path.name, path.read_text())
        print(f"  -> {count} chunks embedded")

    print("Done.")


if __name__ == "__main__":
    main()
