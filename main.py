import requests
from datetime import datetime, date, timedelta
import os
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
    if price < 0:
        return '\U0001F535'  # Blue circle
    elif price < 10:
        return '\U0001F7E2'  # Green circle
    elif price < 23:
        return '\U0001F7E1'  # Yellow circle
    elif price <= 28:
        return '\U0001F534'  # Red circle
    else:
        return '\U000026AB'  # Grey circle

def get_existing_event_times(filename="octopus_agile_event.ics"):
    """Read the .ics file and return a set of (DTSTART, DTEND) tuples for existing events."""
    if not os.path.exists(filename):
        return set()
    event_times = set()
    with open(filename, "r") as f:
        lines = f.readlines()
    dtstart, dtend = None, None
    for line in lines:
        if line.startswith("DTSTART:"):
            dtstart = line.strip().split("DTSTART:")[1]
        if line.startswith("DTEND:"):
            dtend = line.strip().split("DTEND:")[1]
        if line.startswith("END:VEVENT") and dtstart and dtend:
            event_times.add((dtstart, dtend))
            dtstart, dtend = None, None
    return event_times

def get_existing_events_content(filename="octopus_agile_event.ics"):
    """Return the content of all existing VEVENT blocks as a string."""
    if not os.path.exists(filename):
        return ""
    with open(filename, "r") as f:
        lines = f.readlines()
    in_event = False
    event_lines = []
    for line in lines:
        if line.startswith("BEGIN:VEVENT"):
            in_event = True
            event_block = []
        if in_event:
            event_block.append(line)
        if line.startswith("END:VEVENT"):
            in_event = False
            event_lines.append("".join(event_block))
    return "".join(event_lines)

def save_events_to_ics_no_duplicates(results, filename="octopus_agile_event.ics"):
    calendar_header = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Your Product//Your App//EN\n"
    calendar_footer = "END:VCALENDAR\n"
    existing_times = get_existing_event_times(filename)
    existing_events_content = get_existing_events_content(filename)
    print(f"Found {len(existing_times)} existing events in file.")
    # Get now and tomorrow's date in UK local time
    now_uk = datetime.now(tz_london)
    today_uk = now_uk.date()
    tomorrow_uk = (now_uk + timedelta(days=1)).date()
    new_events = ""
    new_count = 0
    for item in results:
        price = item['value_inc_vat']
        valid_from = item['valid_from']
        valid_to = item['valid_to']
        dt_from_utc = datetime.fromisoformat(valid_from.replace('Z', '+00:00'))
        dt_to_utc = datetime.fromisoformat(valid_to.replace('Z', '+00:00'))
        try:
            dt_from_local = dt_from_utc.astimezone(tz_london)
            dt_to_local = dt_to_utc.astimezone(tz_london)
        except Exception:
            dt_from_local = pytz.utc.localize(dt_from_utc).astimezone(tz_london)
            dt_to_local = pytz.utc.localize(dt_to_utc).astimezone(tz_london)
        dtstart = dt_from_local.strftime('%Y%m%dT%H%M%S')
        dtend = dt_to_local.strftime('%Y%m%dT%H%M%S')
        if (dtstart, dtend) in existing_times:
            continue  # Skip duplicate
        uid = datetime.now().strftime('%Y%m%dT%H%M%S%fZ')
        dtstamp = datetime.now().strftime('%Y%m%dT%H%M%SZ')
        icon = get_price_icon(price)
        summary = f"{icon} {price}p"
        event = f"""BEGIN:VEVENT\nUID:{uid}\nDTSTAMP:{dtstamp}\nDTSTART:{dtstart}\nDTEND:{dtend}\nSUMMARY:{summary}\nEND:VEVENT\n"""
        new_events += event
        new_count += 1
    print(f"Adding {new_count} new events.")
    all_events = existing_events_content + new_events
    ics_content = calendar_header + all_events + calendar_footer
    with open(filename, "w") as f:
        f.write(ics_content)
    print(f"All events saved to {filename}")
    # Automatically open the .ics file with the default calendar app (macOS)
    import subprocess
    subprocess.run(["open", filename])
def main():
    results = fetch_octopus_agile_rates()
    save_events_to_ics_no_duplicates(results, "octopus_agile_event.ics")

if __name__ == "__main__":
    main()

