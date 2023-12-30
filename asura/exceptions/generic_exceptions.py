
class MissingParametersException(Exception):
    """
    Thrown when a POST request body has missing fields
    """
    def __init__(self, fields: list):
        super().__init__("Missing field(s): %s" % (fields))