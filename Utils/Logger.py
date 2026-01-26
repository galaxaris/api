import logging
import sys


class CustomFormatter(logging.Formatter):
    """Ajoute des couleurs pour la console (facultatif mais recommandé)."""
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - [%(levelname)s] - %(name)s : %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)


def get_logger(name: str):
    """Fonction utilitaire pour récupérer un logger configuré."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Handler pour la console
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)

        # Handler pour un fichier (utile pour débugger après un crash)
        fh = logging.FileHandler("game_debug.log", mode='w')
        file_fmt = logging.Formatter("%(asctime)s - [%(levelname)s] - %(name)s : %(message)s")
        fh.setFormatter(file_fmt)
        logger.addHandler(fh)

    return logger