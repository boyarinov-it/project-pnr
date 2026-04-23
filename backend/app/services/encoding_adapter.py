from app.core.standard_profile import STANDARD_PROFILE


def get_default_export_encoding() -> str:
    return STANDARD_PROFILE["export"]["default_encoding"]


def get_supported_export_encodings() -> list[str]:
    return STANDARD_PROFILE["export"]["supported_encodings"]


def encode_export_content(content: str, encoding: str | None = None) -> bytes:
    selected_encoding = encoding or get_default_export_encoding()

    if selected_encoding not in get_supported_export_encodings():
        raise ValueError(f"Unsupported export encoding: {selected_encoding}")

    return content.encode(selected_encoding)
