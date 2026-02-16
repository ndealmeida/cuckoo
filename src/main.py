import logging

from injector import Injector

from src.indexer import Indexer
from src.reports import SearchReporter

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    logger.info("Powering up Cuckoo...")
    container = Injector()

    # 1. Start Indexation
    indexer = container.get(Indexer)
    indexer.run_all()

    # 2. Call for Reports
    reporter = container.get(SearchReporter)
    reporter.run_comparison("engineering")


if __name__ == "__main__":
    main()
