import hashlib


def verify_file_signature(file_path: str, expected_signature_hex: str) -> bool:
    digest = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest() == expected_signature_hex.lower()


async def check_for_updates() -> dict:
    return {
        "available": False,
        "version": "0.0.1",
        "message": "No signed update available."
    }
