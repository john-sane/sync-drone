import neopixel
import board
from models.led import Led

class LedStick:
    def __init__(self, pin, database):
        self.led_strip = neopixel.NeoPixel(pin=pin, n=8, brightness=1, pixel_order=neopixel.RGB)
        self.leds = []

        def allocate_leds(self):
            for i in range(8):
                self.leds.add(Led(database, i))

        allocate_leds()

    def set_color(self,  r, g, b, position=None):
        if position is not None:
            self.led_strip.fill((r, g, b), position, 1)
        else:
            self.led_strip.fill((r,g,b))
