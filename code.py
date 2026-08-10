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

while True:
    if not btn1.value:
        # Debounce
        time.sleep(0.3)
        while not btn1.value:
            pass
        print("btn 1 pressed!!!")
        if RECORDING:
            RECORDING = False
            print("stoping recording")
        else:
            RECORDING = True
            print("starting recording")
        led.value = LED_ON if RECORDING else LED_OFF
        # led.value = LED_ON
    time.sleep(0.2)  # Write your code here :-)

    print("btn 3 value: " + str(btn1.value))
    print("RECORDING " + str(RECORDING))
