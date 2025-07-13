#!/usr/bin/env python3
"""
Octopus Agile Calendar Generator

A Python script that fetches Octopus Energy Agile tariff prices and generates
calendar events for easy price tracking. Perfect for budget-conscious consumers
who want to optimize their electricity usage based on real-time pricing.

Author: Budget-conscious student
License: MIT
GitHub: https://github.com/yourusername/octopus-agile-calendar
"""

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
    """
    Fetch current Agile tariff rates from Octopus Energy API.
    
    Returns:
        list: List of pricing data with timestamps and values
        
    Note:
        Currently configured for East Midlands region (tariff code B).
        To use for other regions, modify the URL with appropriate tariff code:
        - London: E-1R-AGILE-24-10-01-A
        - South East: E-1R-AGILE-24-10-01-B
        - etc.
    """
    url = "https://api.octopus.energy/v1/products/AGILE-24-10-01/electricity-tariffs/E-1R-AGILE-24-10-01-B/standard-unit-rates/"
    response = requests.get(url)
    data = response.json()
    return data['results']

def get_price_icon(price):
    """
    Get an appropriate emoji icon based on electricity price.
    
    Args:
        price (float): Price in pence per kWh
        
    Returns:
        str: Unicode emoji representing price level
        
    Price thresholds:
        - Negative: Blue circle (you get paid!)
        - 0-10p: Green circle (very cheap)
        - 10-23p: Yellow circle (moderate)
        - 23-28p: Red circle (expensive)
        - 28p+: Black circle (very expensive)
    """
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
    """
    Read the existing .ics file and extract event time ranges to prevent duplicates.
    
    Args:
        filename (str): Path to the .ics calendar file
        
    Returns:
        set: Set of (DTSTART, DTEND) tuples for existing events
    """
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
    """
    Extract all existing VEVENT blocks from the calendar file.
    
    Args:
        filename (str): Path to the .ics calendar file
        
    Returns:
        str: Combined content of all existing VEVENT blocks
    """
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
    """
    Save pricing events to iCalendar file, avoiding duplicates.
    
    Args:
        results (list): List of pricing data from Octopus API
        filename (str): Output filename for the calendar file
        
    Features:
        - Prevents duplicate events by checking existing timestamps
        - Converts UTC times to UK local time (handles BST/GMT)
        - Adds visual price indicators in event summaries
        - Automatically opens the calendar file on macOS
    """
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
        
        # Convert UTC timestamps to datetime objects
        dt_from_utc = datetime.fromisoformat(valid_from.replace('Z', '+00:00'))
        dt_to_utc = datetime.fromisoformat(valid_to.replace('Z', '+00:00'))
        
        # Convert to UK local time (handles BST/GMT automatically)
        try:
            dt_from_local = dt_from_utc.astimezone(tz_london)
            dt_to_local = dt_to_utc.astimezone(tz_london)
        except Exception:
            # Fallback for older Python versions
            dt_from_local = pytz.utc.localize(dt_from_utc).astimezone(tz_london)
            dt_to_local = pytz.utc.localize(dt_to_utc).astimezone(tz_london)
        
        # Format for iCalendar
        dtstart = dt_from_local.strftime('%Y%m%dT%H%M%S')
        dtend = dt_to_local.strftime('%Y%m%dT%H%M%S')
        
        # Skip if this event already exists
        if (dtstart, dtend) in existing_times:
            continue
        
        # Generate unique identifiers
        uid = datetime.now().strftime('%Y%m%dT%H%M%S%fZ')
        dtstamp = datetime.now().strftime('%Y%m%dT%H%M%SZ')
        
        # Create event summary with price icon and value
        icon = get_price_icon(price)
        summary = f"{icon} {price}p"
        
        # Create iCalendar event
        event = f"""BEGIN:VEVENT\nUID:{uid}\nDTSTAMP:{dtstamp}\nDTSTART:{dtstart}\nDTEND:{dtend}\nSUMMARY:{summary}\nEND:VEVENT\n"""
        new_events += event
        new_count += 1
    
    print(f"Adding {new_count} new events.")
    
    # Combine existing and new events
    all_events = existing_events_content + new_events
    ics_content = calendar_header + all_events + calendar_footer
    
    # Write to file
    with open(filename, "w") as f:
        f.write(ics_content)
    print(f"All events saved to {filename}")
    
    # Automatically open the .ics file with the default calendar app (macOS)
    try:
        import subprocess
        subprocess.run(["open", filename])
    except Exception as e:
        print(f"Could not auto-open calendar file: {e}")
        print(f"Please manually open {filename} to import the events.")

def main():
    """
    Main function to fetch prices and generate calendar.
    
    This function orchestrates the entire process:
    1. Fetches current Agile pricing data from Octopus Energy
    2. Processes the data and converts to calendar events
    3. Saves to .ics file while avoiding duplicates
    4. Attempts to auto-open the calendar file
    """
    print("🐙 Octopus Agile Calendar Generator")
    print("Fetching current pricing data...")
    
    try:
        results = fetch_octopus_agile_rates()
        print(f"Retrieved {len(results)} pricing periods.")
        save_events_to_ics_no_duplicates(results, "octopus_agile_event.ics")
        print("✅ Calendar generation complete!")
        print("\n💡 Tip: Set up this script to run automatically every few hours")
        print("   to keep your calendar updated with the latest prices.")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()

