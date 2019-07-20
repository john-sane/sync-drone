from time import sleep

from models.tag import Tag
from models.led_stick import LedStick
from models.objectbox_models import Tag as TagModel

from pypozyx.core import PozyxConnectionError


# The main class - There should be always only one Drone instance
class Drone:
    def __init__(self, anchors, database, isMaster):
        # init the Drone as inactive
        self.active = False

        # init the database
        self.database = database

        self.isMaster = isMaster

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

        # init anchors
        self.anchors = anchors

        # class, that communicates with the flight controller
        self.control = None
        # current position of the drone (x, y, z)
        self.position = None
        # current orientation of the drone (yaw, roll, pitch)
        self.orientation = None

        # create a Tag in the database and saves the id of the drone tag objects entity
        self.tag_id = database.tag.put(TagModel())

        # create the Tag entity - easy read and write
        self.tag_object = database.tag.get(self.tag_id)

        if self.tag is not None:
            # setup for the Tag
            self.tag.setup()

        # init LED-Stick
        self.led_sticks = LedStick(self.tag_id, database)

    def startUpdateLoop(self):
        # set the Drone as active
        self.active = True
        while self.active:
            self.updatePosition()
            sleep(0.2)
            if self.position is not None:
                # saves the position in the database
                self.savePositionToDatabase()
                self.tag_object.printPosition()
                if self.isMaster:
                    self.updateLEDsFromPosition(self.database)
                self.led_sticks.setColorFromDatabase(self.database)

            if self.orientation is not None:
                # saves the orientation in the database
                self.saveOrientationToDatabase()
                self.tag_object.printOrientation()

    def updateLEDsFromPosition(self, database):
        # get saved postions from database
        position = database.tag.get(self.tag_id).getPosition()

        # get the max values from the anchor coordinates
        max_x = max(self.anchors[0][2], self.anchors[1][2], self.anchors[2][2], self.anchors[3][2])
        max_y = max(self.anchors[0][3], self.anchors[1][3], self.anchors[2][3], self.anchors[3][3])
        max_z = max(self.anchors[0][4], self.anchors[1][4], self.anchors[2][4], self.anchors[3][4])

        # calculate the color depends on the position [coordinate * factor = 255]
        r = position["x"] * (255/max_x)
        g = position["y"] * (255/max_y)
        b = position["z"] * (255/max_z)

        # set the color values
        self.led_sticks.updateColorFromPosition(r, g, b)
        # save color to database
        self.led_sticks.saveColorToDatabase(database)

    def updatePosition(self):
        if self.tag is not None:
            # update position & orientation from the Tag
            self.position = self.tag.getPosition()
            # ToDo: merge OpenCV and Pozyx orientation
            self.orientation = self.tag.getOrientation()
        else:
            # load mocked classes for testing
            self.position = Tag.mockedPosition()
            self.orientation = Tag.mockedOrientation()

        if self.yaw_detector is not None and self.yaw_detector.initVideocapture():
            # Merge detected Angle with pozyx Angle
            print("yaw detector angle: ", self.yaw_detector.getAngle())

    def savePositionToDatabase(self):
        self.tag_object = self.database.tag.get(self.tag_id)
        self.tag_object.setPosition(self.position.x, self.position.y, self.position.z)
        # update position in database object
        self.database.tag.put(self.tag_object)

    def saveOrientationToDatabase(self):
        self.tag_object.setOrientation(self.orientation.heading, self.orientation.roll, self.orientation.pitch)
        # update orientation in database object
        self.database.tag.put(self.tag_object)
