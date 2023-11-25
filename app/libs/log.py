import logging

logging.basicConfig(
    datefmt="%Y-%m-%d:%H:%M:%S",
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
