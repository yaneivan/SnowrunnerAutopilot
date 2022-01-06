import time, keyboard, math
import numpy as np
import cv2
from getVid import WindowCapture

forward = True
time_const = 1
time.sleep(3)
window_name = "Snowrunner"   #check me
standard_pos = False
lower_marker_color = np.array([99, 81, 4])	#bgr
upper_marker_color = np.array([101, 85, 8])

if standard_pos:
	hwnd = win32gui.FindWindow(None, window_name)
	win32gui.MoveWindow(hwnd, -1920, 0, 960, 550, True)

wincap = WindowCapture(window_name)

def toggle_forward():
	global forward
	forward = not(forward)
	if forward:
		keyboard.press('w')
	elif not(forward):
		keyboard.release('w')

def press_buttonz(i, t):
	keyboard.press('w')
	if i == 'L':
		keyboard.press("a")
		time.sleep(t)
		keyboard.release("a")

		keyboard.release("d")
	if i == 'R':
		keyboard.press("d")
		time.sleep(t)
		keyboard.release("d")

		keyboard.release("a")
	if i == 'None':
		keyboard.release("a")
		keyboard.release("d")
last_command = 'None'
last_t = 0.01
last_x_position = 0.5
loop_time = time.time() #for fps
while True:
	img = wincap.get_screenshot()

	mask = cv2.inRange(img, lower_marker_color, upper_marker_color)
	coord = cv2.findNonZero(mask)
	try:
		img = cv2.circle(img, (coord[0][0][0], coord[0][0][1]), 50, (0, 0, 255), 40)
		marker_x_position = coord[0][0][0] / img.shape[1]
		t = math.fabs(marker_x_position - 0.5) * time_const
		if last_t == 0:
			last_t = 0.01
		speed = (last_x_position - marker_x_position) / last_t
		if marker_x_position > 0.55:
			command = 'R'
		elif marker_x_position < 0.45:
			command = 'L'
		else:
			command = 'None'

		if speed > 0.3:
			command = 'None'
		elif speed < -0.3:
			command = 'None'

		press_buttonz(command, t)
		print('command:', command, 'power:', t)

		last_command = command
		last_t = t
		last_x_position = marker_x_position
	except Exception as e:
		keyboard.release('w')
		print(e)

	cv2.imshow('game', img)
	pressed_key = cv2.waitKey(1)
	if pressed_key == ord('q'):
		cv2.destroyAllWindows()
		keyboard.release('w')
		break
	elif pressed_key == 119: # this is w 
		toggle_forward()