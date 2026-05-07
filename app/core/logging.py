import logging


#Configure root logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

#Shared application logger
logger = logging.getLogger("ARIP")