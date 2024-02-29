import pytz, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class DateFormat:
    def __init__(self, date: datetime):
        self.date = date

    @classmethod
    def to_string(self, date: datetime) -> str:
        return datetime.strftime(date, "%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_iso(cls, date: str) -> "DateFormat":
        if date.endswith("Z"):
            date = date[:-1]
        return cls(datetime.fromisoformat(date))

    @classmethod
    def from_timestamp(cls, date: str) -> "DateFormat":
        return cls(datetime.utcfromtimestamp(int(date) / 1000.0))

    def to_local(self) -> datetime:
        tz = pytz.timezone(os.environ.get("TZ", "UTC"))
        return self.date.astimezone(tz)

    def as_datetime(self) -> datetime:
        return self.date
