# 🐙 Octopus Agile Calendar Generator

A Python tool that automatically fetches Octopus Energy Agile tariff prices and generates calendar events for easy price tracking. Perfect for budget-conscious consumers who want to optimize their electricity usage based on real-time pricing.

![Price Calendar Example](https://github.com/user-attachments/assets/09fc3aa6-37c5-43f6-a8c8-967f0757898f)

## 🚀 Features

- **Real-time Price Fetching**: Automatically retrieves current Agile tariff prices from Octopus Energy API
- **Visual Price Indicators**: Color-coded icons for easy price identification at a glance
  - 🔵 Blue: Negative prices (you get paid to use electricity!)
  - 🟢 Green: Very cheap (< 10p/kWh)
  - 🟡 Yellow: Moderate (10-23p/kWh)
  - 🔴 Red: Expensive (23-28p/kWh)
  - ⚫ Black: Very expensive (> 28p/kWh)
- **Duplicate Prevention**: Smart detection to avoid duplicate calendar entries
- **Cross-Platform**: Works on any system with Python
- **macOS Automation**: Includes AppleScript for seamless calendar integration
- **No API Key Required**: Uses public Octopus Energy endpoints
- **Customizable**: Easy to modify for different UK regions

## 📋 Requirements

- Python 3.6+
- Required packages:
  - `requests`
  - `datetime` (built-in)
  - `zoneinfo` (Python 3.9+) or `pytz` (fallback)

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/octopus-agile-calendar.git
cd octopus-agile-calendar
```

2. Install required dependencies:
```bash
pip install requests pytz
```

3. Run the script:
```bash
python main.py
```

## 🎯 Usage

### Basic Usage

Simply run the main script:
```bash
python main.py
```

The script will:
1. Fetch the latest Agile tariff prices for East Midlands
2. Generate an `octopus_agile_event.ics` file
3. Automatically open the calendar file (macOS only)

### Customizing for Different Regions

To use this tool for different UK regions, modify the URL in the `fetch_octopus_agile_rates()` function:

```python
# Current URL for East Midlands
url = "https://api.octopus.energy/v1/products/AGILE-24-10-01/electricity-tariffs/E-1R-AGILE-24-10-01-B/standard-unit-rates/"

# For other regions, replace the tariff code:
# London: E-1R-AGILE-24-10-01-A
# South East: E-1R-AGILE-24-10-01-B
# etc.
```

### macOS Automation

For complete automation on macOS:

1. Set up the Python script to run automatically (using cron, launchd, or Automator)
2. Use the included AppleScript to automatically import events into a specific calendar
3. Modify the calendar name in the AppleScript:
   ```applescript
   click menu item "Your Calendar Name" of menu 1 of calendarPopup
   ```

## 📁 Project Structure

```
octopus-agile-calendar/
├── main.py                    # Main Python script
├── automation.applescript     # AppleScript for macOS automation
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
├── .gitignore                # Git ignore rules
└── octopus_agile_event.ics   # Generated calendar file (excluded from git)
```

## 🔧 Configuration

### Price Thresholds

You can customize the price thresholds by modifying the `get_price_icon()` function:

```python
def get_price_icon(price):
    if price < 0:
        return '\U0001F535'  # Blue circle
    elif price < 10:
        return '\U0001F7E2'  # Green circle
    # ... modify thresholds as needed
```

### Calendar Properties

The generated calendar uses standard iCal format with these properties:
- **PRODID**: Identifies the product that created the calendar
- **VERSION**: iCalendar version (2.0)
- **VEVENT**: Individual price events with start/end times

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- Add support for more UK regions
- Improve the automation scripts
- Add unit tests
- Enhance error handling
- Create a GUI interface

## 📜 License

This project is open source and available under the MIT License.

## 🔒 Privacy & Security

- **No API Keys Required**: Uses public Octopus Energy endpoints
- **No Personal Data**: Script only fetches public pricing information
- **Local Processing**: All data processing happens on your device

## 🆘 Troubleshooting

### Common Issues

1. **Calendar not opening automatically**
   - Ensure you're on macOS and have default calendar app set
   - Try opening the `.ics` file manually

2. **No events appearing**
   - Check your internet connection
   - Verify the Octopus Energy API is accessible
   - Ensure the tariff URL is correct for your region

3. **Duplicate events**
   - The script automatically prevents duplicates
   - Delete the existing `.ics` file to start fresh if needed

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your Python version and dependencies
3. Open an issue on GitHub with detailed error information

## 💡 Tips for Optimal Usage

1. **Schedule Regular Updates**: Set up the script to run every few hours for the latest prices
2. **Monitor Patterns**: Use the calendar to identify the cheapest times for high-energy activities
3. **Share with Friends**: Generate the calendar and share it with others who have Octopus Agile
4. **Backup Your Calendar**: The `.ics` file contains all your price history

## 🌟 Why This Project?

Created by a budget-conscious student, this tool helps Octopus Energy customers:
- Save money by timing electricity usage during cheap periods
- Avoid expensive peak hours
- Take advantage of negative pricing periods
- Plan ahead with visual price indicators

---

**Note**: This is an unofficial tool and is not affiliated with Octopus Energy. Please refer to official Octopus Energy documentation for authoritative pricing information.


