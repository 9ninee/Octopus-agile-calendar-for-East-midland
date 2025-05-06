import requests
from datetime import datetime, date, timedelta
# Try to use zoneinfo (Python 3.9+), fallback to pytz if not available
try:
    from zoneinfo import ZoneInfo
    tz_london = ZoneInfo("Europe/London")
except ImportError:
    import pytz
    tz_london = pytz.timezone("Europe/London")
    
def fetch_octopus_agile_rates():
    url = "https://api.octopus.energy/v1/products/AGILE-24-10-01/electricity-tariffs/E-1R-AGILE-24-10-01-B/standard-unit-rates/"
    response = requests.get(url)
    data = response.json()
    return data['results']

def get_price_icon(price):
    if price < 10:
        return '\U0001F7E2'  # Green circle
    elif price < 23:
        return '\U0001F7E1'  # Yellow circle
    elif price <= 28:
        return '\U0001F534'  # Red circle
    else:
        return '\U000026AB'  # Grey circle

def save_events_to_ics(results, filename="octopus_agile_event.ics"):
    calendar_header = """BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Your Product//Your App//EN\n"""
    calendar_footer = "END:VCALENDAR\n"
    # Get now and tomorrow's date in UK local time
    now_uk = datetime.now(tz_london)
    today_uk = now_uk.date()
    tomorrow_uk = (now_uk + timedelta(days=1)).date()
    events = ""
    for item in results:
        price = item['value_inc_vat']
        valid_from = item['valid_from']
        valid_to = item['valid_to']
        # Convert UTC time to Europe/London local time (handles DST)
        dt_from_utc = datetime.fromisoformat(valid_from.replace('Z', '+00:00'))
        dt_to_utc = datetime.fromisoformat(valid_to.replace('Z', '+00:00'))
        try:
            dt_from_local = dt_from_utc.astimezone(tz_london)
            dt_to_local = dt_to_utc.astimezone(tz_london)
        except Exception:
            dt_from_local = pytz.utc.localize(dt_from_utc).astimezone(tz_london)
            dt_to_local = pytz.utc.localize(dt_to_utc).astimezone(tz_london)
        # Only include events from today 23:00 onwards and all of tomorrow
        if (dt_from_local.date() == today_uk and dt_from_local.hour < 23):
            continue
        if (dt_from_local.date() != today_uk and dt_from_local.date() != tomorrow_uk):
            continue
        dtstart = dt_from_local.strftime('%Y%m%dT%H%M%S')
        dtend = dt_to_local.strftime('%Y%m%dT%H%M%S')
        uid = datetime.now().strftime('%Y%m%dT%H%M%S%fZ')
        dtstamp = datetime.now().strftime('%Y%m%dT%H%M%SZ')
        icon = get_price_icon(price)
        summary = f"{icon} {price}p"
        event = f"""BEGIN:VEVENT\nUID:{uid}\nDTSTAMP:{dtstamp}\nDTSTART:{dtstart}\nDTEND:{dtend}\nSUMMARY:{summary}\nEND:VEVENT\n"""
        events += event
    ics_content = calendar_header + events + calendar_footer
    with open(filename, "w") as f:
        f.write(ics_content)
    print(f"All events saved to {filename}")
    # Automatically open the .ics file with the default calendar app (macOS)
    import subprocess
    subprocess.run(["open", filename])

# Example usage
results = fetch_octopus_agile_rates()
save_events_to_ics(results)

