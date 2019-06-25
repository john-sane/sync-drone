from pypozyx import Coordinates
from pypozyx.core import PozyxConnectionError
import board
import random
from models.tag import Tag
from models.objectbox_models import Tag as TagModel


# The main class - There should be always only one Drone instance
class Drone:
    def __init__(self, anchors, database):

        self.active = False       #initialtes the Drone as inactive

        self.database = database

        try:
            self.tag = Tag(anchors)             # The tag, that tracks the Drone (pozyx)
        except PozyxConnectionError:
            print("No Pozyx Anchor found - will mock up position for tests.")
            self.tag = None            # if no tag found, set it to None

        try:
            from models.yaw_detection import YawDetection
            self.yaw_detector = YawDetection()  # yaw angle
        except ModuleNotFoundError:
            print("couldn't start camera and opencv")
            self.yaw_detector = None            # if opencv fails, set detector None

        self.control = None                     # The class, that communicates with the flight controller
        self.position = None                    # the current position of the drone (easy access)
        self.orientation = None
        # Creates a tag in the database and saves the id of the drone objects entity
        self.tag_id = database.tag.put(TagModel())
        self.db_object = database.tag.get(self.tag_id)  # The entity - easy read and write
        self.led_sticks = {"fl": None,"fr": None, "bl": None, "br": None } # sticks zB fl: front-left

        if self.tag is not None:
            self.tag.setup()  # Setup the Tag

        def initLedSticks(self, pin, stick_position):
            self.led_sticks[stick_position] = LedStick(pin, self.database)

        initLedSticks(board.D18, "fl")


    def startUpdateLoop():
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

    def updateLeds():
        led_sticks["fl"].set_color(random.randint(0, 255),random.randint(0, 255), random.randint(0, 255))

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
