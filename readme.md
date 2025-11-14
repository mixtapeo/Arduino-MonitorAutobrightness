# Auto Brightness Control

An Arduino-based automatic brightness control system that adjusts monitor brightness based on ambient light sensor readings.

https://github.com/user-attachments/assets/1904bc15-6403-4a0b-95c4-2dbb4e4810ad

## Setup Process

### 1. Monitor Feature Code Discovery
- Used **NirSoft's ControlMyMonitor** to find feature codes for monitors:
  - XG27AQDMG
  - KG241Q P
- Tool: https://www.nirsoft.net/utils/control_my_monitor.html

### 2. DDC/CI Utility Setup
- Compiled **winddcutil** for Windows from their GitHub repository
- Repository: https://github.com/scottaxcell/winddcutil
- Uses Windows' SetVCP function to control monitor brightness via DDC/CI protocol

### 3. Usage Example
1. Run Ino with given code (autobrightness.ino)
2. Run brightnesscontrol.py - should be changing brightness now

## Requirements
- Python 3.19.3
- Arduino with light sensor (I used an Uno R4 Wifi)
- Windows OS with DDC/CI capable monitors

## How It Works
1. Arduino reads ambient light sensor values
2. Python script collects sensor data over 1.5 second intervals
3. There is a lag between requesting brightness to bet set, and it being set. Large enough to warrant buffering data and using it. Thus:
   1. Calculates median sensor value to provide a well-representive value every interval
4. Maps sensor values (0-1023) to brightness percentage (0-100%) with an offset added for a brighter bias preference.
5. Uses winddcutil to set monitor brightness via DDC/CI

## Files
- `autobrightness.ino` - Arduino sensor code
- `brightnesscontrol.py` - Main brightness control script
- `winddcutil.exe` - DDC/CI utility for Windows
