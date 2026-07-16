
from app.logger import logger

from app.services.ingestion_service import IngestionService

def main():

    logger.info("RetailPulse Data Generator started.")

    service = IngestionService()

    service.run()


if __name__ == "__main__":
    main()