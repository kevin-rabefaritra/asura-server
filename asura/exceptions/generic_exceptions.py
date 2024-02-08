
class MissingParametersException(Exception):
    """
    Thrown when a POST request body has missing fields
    """
    def __init__(self, fields: str or list):
        _fields = fields if isinstance(fields, list) else [fields]
        super().__init__("Missing field(s): %s" % (_fields))


class NoneException(Exception):
    """
    Thrown when a value that is not expected to be None is None
    """
    def __init__(self, value) -> None:
        super().__init__('Value of %s is not defined' % value)
