import board
import digitalio
import time
import usb_hid
from adafruit_debouncer import Debouncer
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import audio


# --- CONFIGURATION ---
DOUBLE_CLICK_MAX_DELAY = 0.5  # seconds between clicks to count as double click
LONG_PRESS_TIME = 3.0         # seconds to count as long press
LED_OFF = True
LED_ON = False
RECORDING = False

# --- STATE VARIABLES ---
last_click_time = 0
click_count = 0
press_start_time = None
long_press_reported = False

# configure led for button
led = digitalio.DigitalInOut(board.GP26)
led.direction = digitalio.Direction.OUTPUT
led.value = LED_OFF

# Configure button
btn1 = digitalio.DigitalInOut(board.GP27)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.DOWN

# Wrap pin in a Debouncer
switch = Debouncer(lambda: not btn1.value)  # True when pressed
kbd = Keyboard(usb_hid.devices)

CFG = None
def configure(cfg):
    print(f"Configuring button callbacks")    
    global CFG
    CFG = cfg
    

def update():
    global last_click_time, click_count, press_start_time
    global long_press_reported, RECORDING

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
            audio.play_beg()
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
                # kbd.send(Keycode.SPACE)
                # audio.play_stop()
            else:
                RECORDING = True
                print("STARTING recording")
                # Send F12 for RECORD PUNCH (start)
                # kbd.send(Keycode.F12)
            led.value = LED_ON if RECORDING else LED_OFF
        elif click_count == 2:
            print("Double click detected!")
            print("Undo detected!")
            # Send Command+Z for undo
            # kbd.send(Keycode.COMMAND, Keycode.Z)
            # audio.play_undo() 
        click_count = 0

    # if CFG and "on_click" in CFG:
         # CFG["on_click"]("clicked")

# cfg["on_event"]("Button configured successfully!")
# def play_sound(frequencies):

#     def run_task(cfg):
#     print(f"Connecting to {cfg['host']}:{cfg['port']}")
#     cfg["on_event"]("Task finished successfully!")

