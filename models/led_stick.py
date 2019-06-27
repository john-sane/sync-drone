import neopixels
from models.led import Led


class LedStick:
    def __init__(self, pin, database):
        # init NeoPixel class with params
        self.led_stick = neopixel.NeoPixel(pin=pin, n=8, brightness=1, pixel_order=neopixel.GRB)
        # init empty list to save Led Objects
        self.leds = []

        def allocateLeds():
            for i in range(8):
                # put LED objects with given stick position in list
                self.leds.append(Led(database, i))

        allocateLeds()

    def setColor(self, r, g, b):
        self.led_stick.fill((r, g, b))
