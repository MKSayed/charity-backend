from datetime import date, datetime, time, timedelta

from src.config import settings


class ECRRefGenerator:
    reference_date = date(2025, 3, 1)

    @classmethod
    def encode_to_16digits_ecr_ref(
        cls, dt: datetime, service_id: int, kiosk_id: int = settings.kiosk_id
    ):
        # Calculate days since Jan 1, 2000
        days_since_ref_date = (dt.date() - cls.reference_date).days

        # Calculate seconds since midnight
        seconds_since_midnight = dt.hour * 3600 + dt.minute * 60 + dt.second

        # Validate inputs
        if not (0 <= days_since_ref_date < 1000000):  # 6 digits max
            raise ValueError("Date out of supported range")
        if not (0 <= service_id < 1000):
            raise ValueError("Service ID must be between 0 and 999")
        if not (0 <= kiosk_id < 100):
            raise ValueError("Kiosk ID must be between 0 and 99")

        # Combine parts into a 16-digit string
        encoded = f"{days_since_ref_date:06d}{seconds_since_midnight:05d}{service_id:03d}{kiosk_id:02d}"

        return encoded

    @classmethod
    def decode_from_16digits_ecr_ref(cls, encoded: str):
        if len(encoded) != 16:
            raise ValueError("Encoded string must be 16 digits")

        # Extract components
        days_since_ref_date = int(encoded[:6])
        seconds_since_midnight = int(encoded[6:11])
        service_id = int(encoded[11:14])
        kiosk_id = int(encoded[14:16])

        # Convert back to datetime
        dt_date = cls.reference_date + timedelta(days=days_since_ref_date)

        hours = seconds_since_midnight // 3600
        minutes = (seconds_since_midnight % 3600) // 60
        seconds = seconds_since_midnight % 60

        dt = datetime.combine(dt_date, time(hours, minutes, seconds))

        return dt, service_id, kiosk_id
