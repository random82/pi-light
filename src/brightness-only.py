from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause

sense = SenseHat()

color = (15,15,15)
step = 16
sense.clear(color)

def clamp(value, min_value = 0, max_value = 255):
    return min(max_value, max(min_value, value))

def incrementColor(color, increment):
    return tuple(clamp(ele + increment) for ele in color)


def pushed_left(event):
    global color
    if event.action != ACTION_RELEASED:
        color = incrementColor(color, step)

def pushed_right(event):
    global color
    if event.action != ACTION_RELEASED:
        color = incrementColor(color, -step)

def refresh():
    sense.clear(color)

sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right
sense.stick.direction_any = refresh
refresh()
pause()