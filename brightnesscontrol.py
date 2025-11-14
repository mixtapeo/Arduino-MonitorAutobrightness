import serial
import time
import subprocess
import statistics

WINDDCUTIL_PATH = "./winddcutil.exe"
BAUD_RATE = 9600
LATENCY = 1500  # ms
OFFSET = 200

# arduino port
ser = serial.Serial("COM5", BAUD_RATE)
time.sleep(2)  # Wait for connection to stabilize

# Use time-based approach instead of counting readings
COLLECTION_TIME = LATENCY / 1000  # Convert ms to seconds (3 seconds)
sensor_value_list = []
start_time = time.time()


def set_brightness(value):
    print(f"Sensor: {sensor_value}, Setting brightness: {brightness}%")
    command_1 = [
        WINDDCUTIL_PATH,
        "setvcp",
        "1",
        "0x10",  # found through nirsoft for my specific monitors
        str(value),
    ]
    command_2 = [
        WINDDCUTIL_PATH,
        "setvcp",
        "2",
        "0x10",  # found through nirsoft for my specific monitors
        str(value),
    ]
    subprocess.run(command_1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(command_2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clamp(n, min_val, max_val):
    return max(min_val, min(n, max_val))

while True:
    try:
        raw = ser.readline().decode().strip()
        if not raw.isdigit():
            continue
        sensor_value = int(raw)
        sensor_value_list.append(sensor_value)

        # Check if 3 seconds have passed since we started collecting
        if time.time() - start_time >= COLLECTION_TIME:            # use median value in the last 3 seconds as reported brightness
            median_sensor_value = statistics.median(sensor_value_list)
            # Map 0–1023 → 0–100 brightness, offset of 200 for my higher brightness preference
            brightness = int((median_sensor_value + OFFSET) / 1023 * 100)
            brightness = clamp(brightness, 0, 100)
            set_brightness(brightness)
            print(f"Median sensor value: {median_sensor_value}, Setting brightness: {brightness}%")
            sensor_value_list.clear()
            start_time = time.time()  # Reset the timer
    except KeyboardInterrupt:
        break
