from random import random

import neopixel
import board
from models.led import Led
from threading import Thread

class LedStick:
    def __init__(self, database, arm_nr, tag_id):
        # init NeoPixel class with params
        #self.pins = [board.D21, board.D18, board.D12, board.MOSI]
        self.arm_nr = arm_nr
        self.tag_id = tag_id

        self.red = 0
        self.green = 0
        self.blue = 0

        self.led_stick = neopixel.NeoPixel(pin=board.D18, n=36, brightness=1, pixel_order=neopixel.GRB)
        # init empty list to save Led Objects

        self.leds = []
        # put LED objects with given stick position in list
        for i in range(36):
            self.leds.append(Led(database, self.tag_id, self.arm_nr, i))


    """def ledLoop(self):
        while True:
            for i in range(8):
                self.led_stick[i] = (self.red, self.green, self.blue)"""

    def setColor(self, r, g, b):
        for i in range(len(self.leds)):
            self.led_stick[i] = (r, g, b)
