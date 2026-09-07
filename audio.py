import pwmio
import board
import time

def play_sound(frequencies):
	buzzer = pwmio.PWMOut(board.GP15, duty_cycle=0, frequency=frequencies[0], variable_frequency=True)
	try:
		for frequency in frequencies:
			buzzer.frequency = frequency
			buzzer.duty_cycle = 32768
			time.sleep(0.12)
			buzzer.duty_cycle = 0
			time.sleep(0.04)
	finally:
		buzzer.deinit()

def play_start():
	play_sound((523, 784))

def play_stop():
	play_sound((784, 523))

def play_undo():
	play_sound((659, 523, 392))

def play_beg():
	play_sound((784, 659, 523, 262))

# demo
# play_start_sound()
# time.sleep(0.5)
# play_stop_sound()
# time.sleep(0.5)
# play_undo_sound()
# time.sleep(0.5)
# play_go_to_beginning_sound()
