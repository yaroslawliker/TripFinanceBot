

def extract_args(line: str) -> list:
    return line.split()[1:]

class ArgumentError (ValueError):
    """Thrown, when the amount of arguments is incorrect while invoking a command."""
    pass