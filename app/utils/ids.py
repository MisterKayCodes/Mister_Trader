def extract_id(callback_data: str, expected_prefix: str) -> int:
    """Extracts an integer ID from callback data with a known prefix."""
    if not callback_data.startswith(expected_prefix + "_"):
        raise ValueError("Invalid callback prefix")

    try:
        return int(callback_data.rsplit("_", 1)[-1])
    except ValueError:
        raise ValueError("Invalid ID in callback")
