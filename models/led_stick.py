from random import random

import neopixel
import board
from models.objectbox_models import Led as LedModel
from threading import Thread

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

        self.led_stick = neopixel.NeoPixel(pin=board.D18, n=36, brightness=1, pixel_order=neopixel.GRB)

    def doColoring(self, r, g, b):
        for i in range(36):
            self.led_stick[i] = (r, g, b)
            #self.led_stick.saveColorToDatabase()

    def saveColorToDatabase(self, database):
        self.led_object.setColor(self.red, self.green, self.blue)
        database.led.put(self.led_object)
        self.led_object.printColor()





