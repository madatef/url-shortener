import secrets
import string


# base62: unambiguous in URLs, no percent-encoding needed
ALPHABET = string.ascii_letters + string.digits
KEY_LENGTH = 7


def generate_key(length: int = KEY_LENGTH) -> str:
    """
    Generate a random short code.

    Uses secrets rather than random: short codes are the only thing guarding
    an unlisted URL, and random's output is reconstructible from enough
    samples. At the default length the keyspace is 62**7 (~3.5e12), so
    collisions are rare enough to handle by retrying.
    """
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))
