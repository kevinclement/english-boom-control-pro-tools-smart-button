# Yeah so, there are four commands that I need. 
#
#   Command space bar=record 
#   Space bar=stop 
#   Enter=back to beginning of song 
#   Command z=undo 
# Plan: single click, start, stop if started, double click undo, LONG press=back to beginning of song.

# If you could make them hit once, twice, three times, and four times, that would work fine. Or if you have a different way to do it. 

import time
import board
import digitalio
import usb_hid
from adafruit_debouncer import Debouncer
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import usb_hid_map as usb

print("KEYBRD BY kevinc loaded")

# --- CONFIGURATION ---
DOUBLE_CLICK_MAX_DELAY = 0.5  # seconds between clicks to count as double click
LONG_PRESS_TIME = 1.0         # seconds to count as long press

LED_OFF = True
LED_ON = False
RECORDING = False

# configure led for button
led = digitalio.DigitalInOut(board.GP26)
led.direction = digitalio.Direction.OUTPUT
led.value = LED_OFF

# Configure button
btn1 = digitalio.DigitalInOut(board.GP27)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.DOWN

# Set up keyboard and mouse.
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# Wrap pin in a Debouncer
switch = Debouncer(lambda: not btn1.value)  # True when pressed

# --- STATE VARIABLES ---
last_click_time = 0
click_count = 0
press_start_time = None
long_press_reported = False

print("Double-click detection started. Press the button...")

while True:
    switch.update()

    # Detect button press start
    if switch.fell:
        press_start_time = time.monotonic()
        long_press_reported = False

        now = press_start_time
        if now - last_click_time <= DOUBLE_CLICK_MAX_DELAY:
            click_count += 1
        else:
            click_count = 1
        last_click_time = now

    # Detect long press while holding
    if not switch.value and press_start_time is not None:
        if not long_press_reported and (time.monotonic() - press_start_time) >= LONG_PRESS_TIME:
            print("Long press detected!")
            long_press_reported = True
            click_count = 0  # Cancel click counting if it's a long press

    # Detect button release
    if switch.rose:
        press_start_time = None

    # Decide between single and double click after timeout
    if press_start_time is None and click_count > 0 and (time.monotonic() - last_click_time) > DOUBLE_CLICK_MAX_DELAY:
        if click_count == 1 and not long_press_reported:
            print("Single click detected!")
        elif click_count == 2:
            print("Double click detected!")
        click_count = 0

    time.sleep(0.01)  # Small delay to reduce CPU usage
    # switch.update()
    
    # # Detect a press event
    # if switch.fell:
    #     now = time.monotonic()
    #     if now - last_click_time <= DOUBLE_CLICK_MAX_DELAY:
    #         click_count += 1
    #     else:
    #         click_count = 1  # reset if too much time passed
    #     last_click_time = now

    # # Detect long press while holding
    # if switch.value and press_start_time is not None:
    #     if not long_press_reported and (time.monotonic() - press_start_time) >= LONG_PRESS_TIME:
    #         print("Long press detected!")
    #         long_press_reported = True
    #         click_count = 0  # Cancel click counting if it's a long press

    # # Detect button release
    # if switch.rose:
    #     press_start_time = None

    # # Check if enough time has passed since last click to decide
    # if click_count > 0 and (time.monotonic() - last_click_time) > DOUBLE_CLICK_MAX_DELAY:
    #     if click_count == 1:
    #         print("Single click detected!")

    #         # # SINGLE CLICK: Send space bar for record/stop
    #         # if RECORDING:
    #         #     RECORDING = False
    #         #     print("STOPPING recording")
    #         # else:
    #         #     RECORDING = True
    #         #     print("STARTING recording")                            
    #         #     # Send F12 for RECORD PUNCH (start)
    #         #     # alternative is usb.COMMAND usb.SPACE
    #         #     # TODO: uncomment before going live
    #         #     #kbd.send(usb.F12)    
    #         led.value = LED_ON if RECORDING else LED_OFF
    #     elif click_count == 2:
    #         print("Double click detected!")
    #     click_count = 0  # reset after reporting

    # time.sleep(0.01)  # Small delay to reduce CPU usage

    # if not btn1.value:
    #     # Debounce
    #     time.sleep(0.3)
    #     while not btn1.value:
    #         pass
    #     if RECORDING:
    #         RECORDING = False
    #         print("stoping recording")
    #     else:
    #         RECORDING = True
    #         print("starting recording")
    #         # Send F12 for RECORD PUNCH (start)
    #         # alternative is usb.COMMAND usb.SPACE
    #         kbd.send(usb.F12)            
    #     led.value = LED_ON if RECORDING else LED_OFF
    #     # led.value = LED_ON
    # time.sleep(0.2)  # Write your code here :-)