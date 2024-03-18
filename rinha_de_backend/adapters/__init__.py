from datetime import datetime, timezone


class DatetimeAdapter:

    def now(self):
        return datetime.now(timezone.utc)
