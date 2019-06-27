import board
import random
from time import sleep

from models.tag import Tag
from models.led_stick import LedStick
from models.objectbox_models import Tag as TagModel

from pypozyx.core import PozyxConnectionError


# The main class - There should be always only one Drone instance
class Drone:
    def __init__(self, anchors, database):
        # init the Drone as inactive
        self.active = False
        # init the database
        self.database = database

        try:
            # init the tag, that tracks the Drone (pozyx)
            self.tag = Tag(anchors)
        except PozyxConnectionError:
            print("No Pozyx Tag found - will mock up position for tests.")
            # if no tag found, set it to None
            self.tag = None

        try:
            from models.yaw_detection import YawDetection
            # import yawDetection class
            self.yaw_detector = YawDetection()
        except ImportError:
            print("couldn't start camera and opencv")
            # if opencv fails, set detector None
            self.yaw_detector = None

        # class, that communicates with the flight controller
        self.control = None
        # the current position of the drone (x, y, z)
        self.position = None
        # the current orientation of the drone (yaw, roll, pitch)
        self.orientation = None

        # creates a tag in the database and saves the id of the drone objects entity
        self.tag_id = database.tag.put(TagModel())
        # create the entity - easy read and write
        self.db_object = database.tag.get(self.tag_id)
        # LED sticks -> front-left, front-right, back-left, back-right
        self.led_sticks = {'fl': None, 'fr': None, 'bl': None, 'br': None}

        if self.tag is not None:
            # setup for the Tag
            self.tag.setup()

        def initLedSticks(self, pin, stick_position):
            # init LED sticks with an LEDStick object
            self.led_sticks[stick_position] = LedStick(pin, self.database)

        initLedSticks(self, board.D18, 'fl')

    def startUpdateLoop(self):
        active = True
        while self.active:
            self.updatePosition()
            sleep(1.0)
            if self.position is not None:
                self.savePositionToDatabase(self.database)
                self.db_object.printPosition()

            if self.orientation is not None:
                self.saveOrientationToDatabase(self.database)
                self.db_object.printOrientation()

            updateLeds()

    def updateLeds(self):
        
        self.led_sticks["fl"].setColor(random.randint(0, 255),random.randint(0, 255), random.randint(0, 255))

    def updatePosition(self):
        if self.tag is not None:
            self.position = self.tag.getPosition()
            # ToDo: merge OpenCV and Pozyx orientation
            self.orientation = self.tag.getOrientation()
        else:
            self.position = Tag.mockedPosition()
            self.orientation = Tag.mockedOrientation()

        if self.yaw_detector is not None and self.yaw_detector.initVideocapture():
            # Merge detected Angle with pozyx Angle
            print(self.yaw_detector.getAngle())

    def savePositionToDatabase(self, database):
        self.db_object.setPosition(self.position.x, self.position.y, self.position.z)
        database.tag.put(self.db_object)

    def saveOrientationToDatabase(self, database):
        self.db_object.setOrientation(self.orientation.heading, self.orientation.roll, self.orientation.pitch)
        database.tag.put(self.db_object)
