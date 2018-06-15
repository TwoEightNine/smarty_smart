import random
import string
import time
import hashlib
import json
import re

MAX_USERS = 1000000000
SEED_EXPIRATION_TIME = 7200

ERROR_FORMAT = '{"error": %d, "message": "%s"}'
RESPONSE_FORMAT = '{"result": %s}'

RESPONSE_1 = RESPONSE_FORMAT % '1'
RESPONSE_EMPTY_LIST = RESPONSE_FORMAT % '[]'
SEED_ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits

ERROR_DICTIONARY = {
    1: "Missed parameter: %s",
    400: "Bad request",
    401: "Authorization required",
    403: "Forbidden",
    404: "Not found",
    405: "Method not allowed",
    500: "Internal server error"
}


def get_time(widened=False):
    return int(time.time() * (1000 if widened else 1))


def sleep(t=.5):
    time.sleep(t)


def get_ui_time(ts):
    return time.ctime(ts)


def get_random_seed(size=random.randint(24, 32)):
    return ''.join(random.SystemRandom().choice(SEED_ALPHABET) for _ in range(size))


def does_seed_match_alphabet(seed):
    for c in seed:
        if c not in SEED_ALPHABET:
            return False
    return True


def get_error_data(e):
    lst = str(e).split(':')[0].split(' ', 1)
    return int(lst[0]), lst[1]


def get_error_by_code(code):
    return ERROR_FORMAT % (code, ERROR_DICTIONARY[code])


def get_extended_error_by_code(code, fmt_tuple):
    return ERROR_FORMAT % (code, ERROR_DICTIONARY[code] % fmt_tuple)

def as_str(s):
    return '"%s"' % s

