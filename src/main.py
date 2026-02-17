import logging
import sys

import uvicorn
from injector import Injector

from src.services import ElasticsearchService, VespaService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    logger.info("Powering up Cuckoo...")
    container = Injector()

    # 1. Health Checks
    if not container.get(ElasticsearchService).test_connection():
        logger.error("Failed to connect to Elasticsearch")
        sys.exit(1)

    vespa_service = container.get(VespaService)
    if not vespa_service.test_connection():
        logger.error("Failed to connect to Vespa Server")
        sys.exit(1)

    uvicorn.run("src.api:app", host="0.0.0.0", port=3000, reload=True)


if __name__ == "__main__":
    main()
