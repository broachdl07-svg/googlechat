from __future__ import annotations

from mautrix.types import MessageType
from mautrix.util import magic
import mimetypes

_GENERIC_MIME_TYPES = {"application/octet-stream", "binary/octet-stream"}


def normalize_mime_type(value: str | None) -> str | None:
    if not value:
        return None
    mime = value.partition(";")[0].strip().lower()
    return mime or None


def choose_mime_type(
    data: bytes,
    *,
    detected: str | None = None,
    hint: str | None = None,
    filename: str | None = None,
) -> str:
    mime = normalize_mime_type(detected)
    if mime and mime not in _GENERIC_MIME_TYPES:
        return mime

    mime = normalize_mime_type(hint)
    if mime and mime not in _GENERIC_MIME_TYPES:
        return mime

    if filename:
        mime = normalize_mime_type(mimetypes.guess_type(filename)[0])
        if mime and mime not in _GENERIC_MIME_TYPES:
            return mime

    mime = normalize_mime_type(magic.mimetype(data))
    if mime:
        return mime

    return normalize_mime_type(detected) or normalize_mime_type(hint) or "application/octet-stream"


def message_type_from_mime(mime: str) -> MessageType:
    msgtype = getattr(MessageType, mime.partition("/")[0].upper(), MessageType.FILE)
    return MessageType.FILE if msgtype == MessageType.TEXT else msgtype
