def excepthook(exctype, value, tb):
    print(f"Uncaught Exception ({exctype}): {value}. Traceback:\n {tb}")


def handle_exception(err: Exception, raise_again=False):
    print(f"exception ({type(err)}) occurred: {err}")
    if raise_again:
        raise err


def handle_error(msg: str):
    print(f"Error occurred: {msg}")
