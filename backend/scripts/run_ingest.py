"""CLI entrypoint: run from backend/ as `python -m scripts.run_ingest`."""

from dotenv import load_dotenv

load_dotenv()

from rag.ingest import ingest_all


def main() -> None:
    ingest_all()
    print("Done.")


if __name__ == "__main__":
    main()
