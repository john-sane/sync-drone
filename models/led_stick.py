from random import random

import neopixel
import board
from models.objectbox_models import Led as LedModel


class LedStick:
    def __init__(self, tag_id, database):
        # init NeoPixel class with params
        # self.pins = [board.D21, board.D18, board.D12, board.MOSI]
        self.tag_id = tag_id
        self.db_id = database.led.put(LedModel())
        self.led_object = database.led.get(self.db_id)
        self.red = 0
        self.green = 0
        self.blue = 0
        self.led_count = 36

        self.led_stick = neopixel.NeoPixel(pin=board.D12, n=self.led_count, brightness=1, pixel_order=neopixel.GRB)

    def updateColorFromPosition(self, r, g, b):
        # set color for
        self.red = self.normalize_range(int(r))
        self.green = self.normalize_range(int(g))
        self.blue = self.normalize_range(int(b))

    @staticmethod
    def normalize_range(value):
        return min(max(value, 0), 255)

    def saveColorToDatabase(self, database):
        # update color in every led database object
        for led in database.led.get_all():
            led.setColor(self.red, self.green, self.blue)
            database.led.put(led)

    def setColorFromDatabase(self, database):
        rgb = database.led.get(self.db_id).getColor()
        self.led_stick.fill((rgb['red'], rgb['green'], rgb['blue']))
        self.led_stick.show()
        print("red: ", rgb['red'], "green: ", rgb['green'], "blue: ", rgb['blue'], "ID: ", self.db_id)



