import logging
import sys

from injector import Injector

from src.services import VespaService

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def deploy():
    container = Injector()
    vespa_service = container.get(VespaService)

    if not vespa_service.test_connection():
        logger.error("❌ Failed to connect to Vespa Config Server.")
        sys.exit(1)

    try:
        logger.info("🚢 Deploying Vespa Application Package...")
        vespa_service.deploy_from_disk()
        logger.info("✅ Vespa deployment complete.")
    except Exception as e:
        logger.error(f"❌ Failed to deploy Vespa: {e}")
        sys.exit(1)


if __name__ == "__main__":
    deploy()
