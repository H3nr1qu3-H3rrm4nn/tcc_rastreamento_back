from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Default timezone assumption for naive datetimes coming from Brazil.
BRAZIL_TZ = ZoneInfo("America/Sao_Paulo")


def normalize_to_utc(value: datetime | str | None, assume_tz: ZoneInfo = BRAZIL_TZ) -> datetime | None:
    """Parse ISO/aware/naive datetime and return timezone-aware UTC.

    - Strings are parsed with datetime.fromisoformat, accepting a trailing "Z".
    - Naive datetimes are assumed to be in the provided timezone (America/Sao_Paulo by default).
    - Returns None when value is None.
    """
    if value is None:
        return None

    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception as exc:  # pragma: no cover - defensive
            raise ValueError("timestamp deve estar em ISO 8601") from exc
    elif isinstance(value, datetime):
        parsed = value
    else:  # pragma: no cover - defensive
        raise TypeError("timestamp deve ser datetime ou str")

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=assume_tz)

    return parsed.astimezone(timezone.utc)
