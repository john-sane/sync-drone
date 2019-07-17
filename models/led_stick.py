from random import random

import neopixel
import board
from models.objectbox_models import Led as LedModel

class LedStick:
    def __init__(self, tag_id, database):
        # init NeoPixel class with params
        #self.pins = [board.D21, board.D18, board.D12, board.MOSI]
        self.tag_id = tag_id
        self.db_id = database.led.put(LedModel())
        self.led_object = database.led.get(self.db_id)
        self.red = 0
        self.green = 0
        self.blue = 0
        self.led_count = 36

        self.led_stick = neopixel.NeoPixel(pin=board.D18, n=self.led_count, brightness=1, pixel_order=neopixel.GRB)

    def doColoring(self, r, g, b):
        # set color for
        for i in range(self.led_count):
            self.led_stick[i] = (r, g, b)
            self.red = self.led_stick[0][0]
            self.green = self.led_stick[0][1]
            self.blue = self.led_stick[0][2]

        print("R", self.red, "G:",  self.green, "B:",  self.blue)
        return self.red, self.green, self.blue

    def saveColorToDatabase(self, database):
        self.led_object.setColor(self.red, self.green, self.blue)
        # update color in database object
        database.led.put(self.led_object)
        database.led.get(self.db_id).printColor()
