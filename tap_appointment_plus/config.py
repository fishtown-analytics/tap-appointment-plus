import json

from tap_appointment_plus.logger import LOGGER as logger
from voluptuous import Schema, Required

CONFIG_CONTRACT = Schema({
    Required('site_id'): str,
    Required('api_key'): str,
    Required('start_date'): str,
    Required('user_agent'): str,
})


def validate(config):
    CONFIG_CONTRACT(config)


def load(filename):
    config = {}

    try:
        with open(filename) as handle:
            config = json.load(handle)
    except:
        logger.fatal("Failed to decode config file. Is it valid json?")
        raise RuntimeError

    validate(config)

    return config
