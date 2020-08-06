from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
import math
import sys
import os

sense = SenseHat()

temperature = 6500
temperature_step = 200
color = (0,0,0)
brightness = 1.0
brightness_step = .1

def clamp(value, min_value = 0, max_value = 255):
    return min(max_value, max(min_value, value))

def adjustBrightness(color, brightness):
    return tuple(clamp(int(ele * brightness)) for ele in color)

def kelvinToRgb(temperature):
    temperature = temperature / 100

    def getRed(temperature):
        if (temperature <= 66) :
            return 255
        else:
            red = temperature - 60
            red = int(329.698727446 * math.pow(red, -0.1332047592))
            return clamp(red)


    def getGreen(temperature):
        if(temperature <= 66):
            green = temperature
            green = int(99.4708025861 * math.log(green) - 161.1195681661)
            return clamp(green)
        else:
            green = temperature - 60
            green = int(288.1221695283 * math.pow(green, -0.0755148492))
            return clamp(green)

    def getBlue(temperature):
        if(temperature >= 66):
            return 255
        else:
            if(temperature <= 19):
                return 0
            else:
                blue = temperature - 10
                blue = int(138.5177312231 * math.log(blue) - 305.0447927307)
                return clamp(blue)
    color = (getRed(temperature), getGreen(temperature), getBlue(temperature))
    print(temperature * 100, 'K ', color)
    return color

def pushed_up(event):
    global temperature
    global color
    if event.action != ACTION_RELEASED:
        temperature += temperature_step
        temperature = clamp(temperature, 1000, 12000)

def pushed_down(event):
    global temperature
    global color
    if event.action != ACTION_RELEASED:
        temperature -= temperature_step
        temperature = clamp(temperature, 1000, 12000)

def pushed_left(event):
    global brightness
    if event.action != ACTION_RELEASED:
        brightness += brightness_step
        brightness = clamp(brightness, 0 , 1)

def pushed_right(event):
    global brightness
    if event.action != ACTION_RELEASED:
        brightness -= brightness_step
        brightness = clamp(brightness, 0 , 1)

def refresh():
    color = kelvinToRgb(temperature)
    color = adjustBrightness(color, brightness)
    sense.clear(color)

def main():

    color = kelvinToRgb(temperature)
    sense.clear(color)

    sense.stick.direction_up = pushed_up
    sense.stick.direction_down = pushed_down
    sense.stick.direction_left = pushed_left
    sense.stick.direction_right = pushed_right
    sense.stick.direction_any = refresh
    refresh()
    pause()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sense.clear()
        print('Closing')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

