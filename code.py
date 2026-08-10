# Yeah so, there are four commands that I need. 
#
#   Command space bar=record 
#   Space bar=stop 
# Enter=back to beginning of song 
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
import pwmio

print("KEYBRD BY kevinc loaded")

# # On the Cytron Maker Pi Pico, the buzzer is hardwired to GP22
# BUZZER_PIN = board.GP18

# # Initialize PWM out on the buzzer pin with variable frequency enabled
# buzzer = pwmio.PWMOut(BUZZER_PIN, variable_frequency=True)

# def play_tone(frequency, duration):
#     """Plays a specific frequency for a given duration in seconds."""
#     if frequency == 0:
#         buzzer.duty_cycle = 0  # Silence
#     else:
#         buzzer.frequency = frequency
#         # 50% duty cycle creates a clean square wave sound (65535 // 2)
#         buzzer.duty_cycle = 32768
    
#     time.sleep(duration)
#     buzzer.duty_cycle = 0  # Turn off sound after duration

# # --- Main Loop ---
# # Scale of frequencies (in Hz) to play: C5, E5, G5, C6
# scale = [523, 659, 784, 1047]

# print("Playing tones...")
# play_tone(1200, 0.1)
# time.sleep(0.08)

# # for freq in scale:
# #     play_tone(freq, 0.3)      # Play note for 300ms
# #     time.sleep(0.1)           # Short pause between notes

# # Final cleanup to ensure it stays quiet
# buzzer.deinit()
# print("Done!")


# --- CONFIGURATION ---
DOUBLE_CLICK_MAX_DELAY = 0.5  # seconds between clicks to count as double click
LONG_PRESS_TIME = 3.0         # seconds to count as long press

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

print("Protools smart control button by kevinc.")

while True:
    switch.update()

    # Detect button press start
    if switch.fell:
        press_start_time = time.monotonic()
        long_press_reported = False

        now = press_start_time
        if now - last_click_time<= DOUBLE_CLICK_MAX_DELAY:
            click_count += 1
        else:
            click_count = 1
        last_click_time = now

    # Detect long press while holding
    if not switch.value and press_start_time is not None:
        if not long_press_reported and (time.monotonic() - press_start_time) >= LONG_PRESS_TIME:
            # Send RETURN for back to beginning of song
            print("LONG, returning to start.")
            kbd.send(Keycode.RETURN)            
            long_press_reported = True
            click_count = 0  # Cancel click counting if it's a long press

    # Detect button release
    if switch.rose:
        press_start_time = None

    # Decide between single and double click after timeout
    if press_start_time is None and click_count > 0 and (time.monotonic() - last_click_time) > DOUBLE_CLICK_MAX_DELAY:
        if click_count == 1 and not long_press_reported:
            print("Single click detected!")
            if RECORDING:
                RECORDING = False
                print("STOPPING recording")
                # Send SPACE to STOP                
                kbd.send(Keycode.SPACE)
            else:
                RECORDING = True
                print("STARTING recording")
                # Send F12 for RECORD PUNCH (start)
                kbd.send(Keycode.F12)
            led.value = LED_ON if RECORDING else LED_OFF
        elif click_count == 2:
            print("Undo detected!")
            # Send Command+Z for undo
            kbd.send(Keycode.COMMAND, Keycode.Z)
        click_count = 0

    time.sleep(0.1)  # Small delay to reduce CPU usage
    