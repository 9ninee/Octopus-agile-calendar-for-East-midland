# 🔌 Octopus Agile Price Calendar — East Midlands

> Automatically fetch half-hourly Octopus Agile electricity prices and import them into your macOS Calendar app — no private API key required.

![Screenshot 2025-07-05 at 18 13 16](https://github.com/user-attachments/assets/09fc3aa6-37c5-43f6-a8c8-967f0757898f)

---

## 📖 Overview

This Python tool fetches real-time half-hourly electricity unit rates from the **[Octopus Energy](https://octopus.energy) Agile tariff API** and generates a `.ics` calendar file. Each 30-minute pricing slot is represented as a calendar event with a colour-coded emoji, making it easy to spot at a glance when electricity is cheapest — ideal for scheduling high-energy tasks like EV charging, washing machines, or dishwashers.

The `.ics` file can be automatically opened and imported into the macOS **Calendar** app via an included **AppleScript**, and the whole workflow can be fully automated using macOS's built-in **Automator** and **Shortcuts** apps — no third-party automation tools needed.

---

## ✨ Features

- 📡 **Live pricing data** from the Octopus Energy public API (no API key required)
- 📅 **`.ics` calendar generation** — compatible with Apple Calendar, Google Calendar, Outlook, and any iCal-compatible app
- 🎨 **Colour-coded emoji indicators** for instant price awareness:
  - 🔵 Negative price (they pay *you*!)
  - 🟢 Under 10p/kWh — great time to use energy
  - 🟡 10p–22p/kWh — moderate price
  - 🔴 23p–28p/kWh — high price
  - ⚫ Over 28p/kWh — very high, avoid if possible
- 🔁 **Duplicate-safe** — re-running the script won't create duplicate calendar entries
- 🍎 **macOS automation ready** — includes AppleScript to auto-import into a named calendar
- 🌍 **Multi-region scalable** — easily adapted for any UK Octopus Agile distribution region

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+ (uses `zoneinfo`; falls back to `pytz` for older versions)
- `requests` library
```bash
pip install requests
# Optional fallback for Python < 3.9:
pip install pytz
```

### Run the script
```bash
python main.py
```

This will:
1. Fetch the latest Agile unit rates from the Octopus API
2. Generate/update `octopus_agile_event.ics` in the same directory
3. Automatically open the file in your default calendar app (macOS)

---

## 🍎 Full macOS Automation (Optional)

To fully automate daily imports into a specific calendar (e.g. "Agile Price"):

1. Schedule `main.py` to run nightly using **Automator** or a `launchd` plist
2. Use the included `Apple_Script` to automatically confirm the import dialog and assign the events to your chosen calendar

The AppleScript handles:
- Selecting the correct calendar from the import popup
- Clicking "OK" to confirm the import

> You can customise the calendar name by editing `"Agile Price"` in the AppleScript.

---

## 🌍 Adapting for Other UK Regions

The script currently uses the **East Midlands** (`B`) distribution region. To switch regions, update the API URL in `main.py`:
```python
url = "https://api.octopus.energy/v1/products/AGILE-24-10-01/electricity-tariffs/E-1R-AGILE-24-10-01-{REGION_CODE}/standard-unit-rates/"
```

Replace `{REGION_CODE}` with your region's letter code. Full region codes are available in the [Octopus Energy API docs](https://developer.octopus.energy/docs/api/#list-tariff-charges).

| Region | Code |
|---|---|
| East Midlands | B |
| Eastern England | A |
| London | C |
| Merseyside & N. Wales | D |
| West Midlands | E |
| North East England | F |
| North West England | G |
| Southern England | H |
| South East England | J |
| South Western England | K |
| Yorkshire | M |
| South Scotland | N |
| North Scotland | P |

---

## 🗺️ Scalability & Future Ideas

This project was built on a budget with simplicity in mind, but it has a clear path to more powerful features:

- **☁️ Calendar server / WebDAV** — host the `.ics` as a live-subscribed calendar so any device updates automatically without manual imports
- **📬 Email/notification delivery** — send the daily price schedule via email or push notification each morning
- **📊 Price analytics** — log historical prices to a local database and visualise cheapest windows over time
- **🤖 Smart home integration** — connect with [Home Assistant](https://www.home-assistant.io/), Apple Shortcuts, or IFTTT to trigger smart plugs at cheap-rate windows
- **🐳 Docker deployment** — containerise for easy scheduling on a Raspberry Pi or home server
- **🌐 Web dashboard** — a lightweight Flask or FastAPI app to display today's prices in a browser

---

## 💡 Quickest Alternative

> Don't want to run this yourself? Share it with a friend who will — and simply **subscribe to their calendar feed**. One person runs the script, everyone benefits.

---

## 🏷️ Related

[#OctopusEnergy](https://octopus.energy) · [#AgileOctopus](https://octopus.energy/agile) · [#HomeAssistant](https://www.home-assistant.io/) · [#OpenEnergyData](https://www.gov.uk/guidance/find-and-use-data-energy) · [#Zapier](https://zapier.com) · [#IFTTT](https://ifttt.com) · [#AppleShortcuts](https://support.apple.com/en-gb/guide/shortcuts/welcome/ios)

---

## 📄 Licence

MIT — free to use, modify, and share.

---

*Built by a student in the East Midlands trying to keep the electricity bill down. 💸*
