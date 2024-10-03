import secrets


def generate_token(hash_len = 16) -> str:
    return secrets.token_hex(hash_len)