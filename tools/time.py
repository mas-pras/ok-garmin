from langchain.tools import tool
from datetime import datetime
import pytz

@tool
def get_time(city: str) -> str:
    """Gibt die aktuelle Uhrzeit in einer angegebenen Stadt zurück. Denke dir keine scheisse aus."""
    try:
        city_timezones = {
            "new york": "America/New_York",
            "london": "Europe/London",
            "tokyo": "Asia/Tokyo",
            "sydney": "Australia/Sydney"
        }
        city_key = city.lower()
        if city_key not in city_timezones:
            return f"Entschuldigung, ich kenne die Zeitzone für {city} nicht."

        timezone = pytz.timezone(city_timezones[city_key])
        current_time = datetime.now(timezone).strftime("%H:%M")
        return f"Die aktuelle Uhrzeit in {city.title()} ist {current_time}."
    except Exception as e:
        return f"Fehler: {e}"
