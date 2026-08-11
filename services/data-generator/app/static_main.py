from app.services.static_ingestion_service import (
    StaticIngestionService,
)


def main() -> None:

    service = StaticIngestionService()

    service.run_stores()


if __name__ == "__main__":
    main()