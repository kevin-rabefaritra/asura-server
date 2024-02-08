import uuid

def generate_hex_uuid() -> str:
    """
    Generates a random hex uuid
    """
    return uuid.uuid4().hex
