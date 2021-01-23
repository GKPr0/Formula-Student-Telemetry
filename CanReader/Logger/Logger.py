import codecs
import json
import logging
import logging.config


def setup_logger():
    config_file = "Logger/LoggerConfig.json"
    with codecs.open(config_file, "r", encoding="utf-8") as cf:
        config = json.load(cf)

    logging.config.dictConfig(config["logging"])