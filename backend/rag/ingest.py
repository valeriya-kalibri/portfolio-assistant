"""Walks kb/**/*.md and upserts each file as one whole-document kb_documents row.

No sub-splitting: each file is already a topic-coherent, self-contained document
sized to fit comfortably within a few retrieved docs' worth of context.
"""

from pathlib import Path

from rag.documents import upsert_kb_document

KB_DIR = Path(__file__).resolve().parent.parent.parent / "kb"

TOPIC_BY_STEM: dict[str, str] = {
    "identity": "identity",
    "career-timeline": "career",
    "kalibri-studios": "venture",
    "skills": "skills",
    "education": "education",
    "press": "press",
    "faq": "faq",
    "personality": "personality",
    "about-this-assistant": "meta",
    "3d-background-details": "3d_background",
}


def _slug_and_topic(path: Path) -> tuple[str, str]:
    if path.parent.name == "projects":
        return f"project-{path.stem}", "project"
    if path.stem not in TOPIC_BY_STEM:
        raise ValueError(f"Unrecognized KB doc {path}: add it to TOPIC_BY_STEM")
    return path.stem, TOPIC_BY_STEM[path.stem]


def _extract_title(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("KB doc is missing a top-level `# Title` line")


def ingest_all() -> None:
    for path in sorted(KB_DIR.rglob("*.md")):
        text = path.read_text().strip()
        slug, topic = _slug_and_topic(path)
        title = _extract_title(text)
        upsert_kb_document(slug=slug, topic=topic, title=title, content=text)
        print(f"Ingested {slug} ({topic})")
