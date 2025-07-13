(*
Octopus Agile Calendar - macOS Automation Script

This AppleScript automates the import of calendar events into a specific calendar
in the macOS Calendar app. It's designed to work with the Octopus Agile calendar
generator to provide seamless integration.

Usage:
1. Ensure the Calendar app is running
2. Make sure you have a calendar named "Agile Price" (or modify the script)
3. Run this script after the Python script generates the .ics file

Note: You may need to adjust the calendar name and timing delays based on your system
*)

## this is for fully automation with the build-in function inside MacOS

## Step 2: Confirm the import dialog
delay 1
tell application "System Events"
	tell process "Calendar"
		repeat 10 times
			if exists window 1 then
				try
					-- Attempt to select the calendar named "Agile Price"
					set calendarPopup to pop up button 1 of window 1
					click calendarPopup
					delay 0.5
					
					-- Select "Agile Price" from the dropdown (Replace with your own calendar name)
					click menu item "Agile Price" of menu 1 of calendarPopup
					
					-- Click the OK button if it exists
					if exists button "OK" of window 1 then
						click button "OK" of window 1
						exit repeat
					end if
				end try
			end if
			delay 0.5
		end repeat
	end tell
end tell

