from pypozyx import Coordinates
from pypozyx.core import PozyxConnectionError
from models.tag import Tag
from models.objectbox_models import Tag as TagModel


# The main class - There should be always only one Drone instance
class Drone:
    def __init__(self, anchors, database):

        try:
            self.tag = Tag(anchors)             # The tag, that tracks the Drone (pozyx)
        except PozyxConnectionError:
            print("No Pozyx Anchor found - will mock up position for tests.")
            self.tag = None                     # if no tag found, set it to None

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
        self.database_id = database.tag.put(TagModel())
        self.db_object = database.tag.get(self.database_id)  # The entity - easy read and write

        if self.tag is not None:
            self.tag.setup()  # Setup the Tag

    def updatePosition(self):
        if self.tag is not None:
            self.position = self.tag.getPosition()
            self.orientation = self.tag.getOrientation()
        else:
            self.position = Tag.mockedPosition()
            self.orientation = Tag.mockedOrientation()

        if self.yaw_detector is not None and self.yaw_detector.initVideocapture():
            self.yaw_detector.getAngle()

    def savePositionToDatabase(self, database):
        self.db_object.setPosition(self.position.x, self.position.y, self.position.z)
        database.tag.put(self.db_object)

    def saveOrientationToDatabase(self, database):
        self.db_object.setOrientation(self.orientation.heading, self.orientation.roll, self.orientation.pitch)
        database.tag.put(self.db_object)
