import time

ERROR_FORMAT = '{"error": %d, "message": "%s"}'

ERROR_DICTIONARY = {
    400: "The request has been performed mistakenly",
    401: "Authorization required",
    403: "Requested resourced cannot be provided",
    404: "Requested resources cannot be found",
    405: "The request has been executed mistakenly",
    500: "The server cannot process the request due to an internal problem"
}


def sleep(t=.5):
    time.sleep(t)


def get_error_data(e):
    lst = str(e).split(':')[0].split(' ', 1)
    return int(lst[0]), lst[1]


def get_error_by_code(code):
    return ERROR_FORMAT % (code, ERROR_DICTIONARY[code])

