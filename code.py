# Yeah so, there are four commands that I need. 
#
#   Command space bar=record 
#   Space bar=stop 
# Enter=back to beginning of song 
#   Command z=undo 
# Plan: single click, start, stop if started, double click undo, LONG press=back to beginning of song.

# Button Wiring: 
#   GP20 = white   => wht/org => dit
#   GP27 = black   => brwn    => dot
#   vbus = yellow  => orange  => dash
#   GP15 = white   => black   => wht/blu => buzzer+  
#   gnd  = blue    => yellow  => blue => buzzer-

# If you could make them hit once, twice, three times, and four times, that would work fine. Or if you have a different way to do it. 
#
import time
import board
import digitalio
import usb_hid
from adafruit_debouncer import Debouncer
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import audio

# --- CONFIGURATION ---
DOUBLE_CLICK_MAX_DELAY = 0.75  # seconds between clicks to count as double click
LONG_PRESS_TIME = 3.0         # seconds to count as long press

LED_OFF = False
LED_ON = True
RECORDING = False

# configure led for button
led = digitalio.DigitalInOut(board.GP20)
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
double_click_pending = False

print("Protools smart control button by kevinc.")

while True:
    # The button and lamp share GP20. Pulse it only for the instant GP27 is
    # sampled when idle; while recording, leave it powered continuously.
    if not RECORDING:
        led.value = LED_ON
    switch.update()
    if not RECORDING:
        led.value = LED_OFF

    # Detect button press start
    if switch.fell:
        press_start_time = time.monotonic()
        long_press_reported = False
        if click_count == 1 and press_start_time - last_click_time <= DOUBLE_CLICK_MAX_DELAY:
            double_click_pending = True

    # Detect long press while holding
    if not switch.value and press_start_time is not None:
        if not long_press_reported and (time.monotonic() - press_start_time) >= LONG_PRESS_TIME:
            # Send RETURN for back to beginning of song            
            print("  <- BEG ")            
            kbd.send(Keycode.RETURN)            
            audio.play_beg()
            long_press_reported = True
            click_count = 0  # Cancel click counting if it's a long press
            double_click_pending = False

    # Detect button release
    if switch.rose:
        if not long_press_reported:
            now = time.monotonic()
            if double_click_pending:
                click_count = 2
                double_click_pending = False
            elif click_count == 0 or now - last_click_time <= DOUBLE_CLICK_MAX_DELAY:
                click_count += 1
            else:
                click_count = 1
            last_click_time = now
        press_start_time = None

    # A double click is known immediately; a single click waits for the timeout.
    if press_start_time is None:
        if click_count >= 2:
            #print("Double click detected!")
            #print("Undo detected!")
            print("  @@ UNDO ")
            # Send Command+Z for undo
            # kbd.send(Keycode.COMMAND, Keycode.Z)
            audio.play_undo()
            click_count = 0
        elif click_count == 1 and (time.monotonic() - last_click_time) > DOUBLE_CLICK_MAX_DELAY:
            # print("Single click detected!")
            if RECORDING:
                RECORDING = False
                print("  << STOP ")
                # Send SPACE to STOP                
                # kbd.send(Keycode.SPACE)
                audio.play_stop()
            else:
                RECORDING = True
                print("  >> START")
                # Send F12 for RECORD PUNCH (start)
                # kbd.send(Keycode.F12)
                audio.play_start()
            led.value = LED_ON if RECORDING else LED_OFF
            print("  LED ON" if RECORDING else "  LED OFF")
            click_count = 0

    time.sleep(0.01)
    