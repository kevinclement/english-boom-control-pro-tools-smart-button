# Yeah so, there are four commands that I need. 
#
#   Command space bar=record 
#   Space bar=stop 
#   Enter=back to beginning of song 
#   Command z=undo 

# If you could make them hit once, twice, three times, and four times, that would work fine. Or if you have a different way to do it. 

import time
import board
import digitalio
import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import usb_hid_map as usb

print("KEYBRD BY kevinc loaded")

LED_OFF = True
LED_ON = False
RECORDING = False
DEBOUNCE_SECONDS = 0.05
DOUBLE_CLICK_SECONDS = 0.5
pending_click_time = None

# configure led for button
led = digitalio.DigitalInOut(board.GP26)
led.direction = digitalio.Direction.OUTPUT
led.value = LED_OFF

# Configure button
btn1 = digitalio.DigitalInOut(board.GP27)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.DOWN
raw_button_value = btn1.value
stable_button_value = raw_button_value
button_change_time = time.monotonic()

# Set up keyboard and mouse.
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

while True:
    button_value = btn1.value
    current_time = time.monotonic()

    if button_value != raw_button_value:
        raw_button_value = button_value
        button_change_time = current_time

    if (raw_button_value != stable_button_value and
            current_time - button_change_time >= DEBOUNCE_SECONDS):
        stable_button_value = raw_button_value
        if stable_button_value:
            if (pending_click_time is not None and
                    current_time - pending_click_time <= DOUBLE_CLICK_SECONDS):
                pending_click_time = None
                print("button double clicked")
            else:
                pending_click_time = current_time

    if (pending_click_time is not None and
            current_time - pending_click_time > DOUBLE_CLICK_SECONDS):
        pending_click_time = None
        if RECORDING:
            RECORDING = False
            print("stoping recording")
        else:
            RECORDING = True
            print("starting recording")
            # Send F12 for RECORD PUNCH (start)
            # alternative is usb.COMMAND usb.SPACE
            kbd.send(usb.F12)
        led.value = LED_ON if RECORDING else LED_OFF
        # led.value = LED_ON
    time.sleep(0.02)  # Write your code here :-)