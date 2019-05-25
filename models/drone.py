from pypozyx import Coordinates
from models.tag import Tag
from models.objectbox_models import Tag as TagModel
from models.yaw_detection import YawDetection


# The main class - There should be always only one Drone instance
class Drone:
    def __init__(self, anchors, database):
        self.tag = Tag(anchors)      # The tag, that tracks the Drone (pozyx)
        self.control = None          # The class, that communicates with the flight controller
        self.position = None         # the current position of the drone (easy access)
        self.euler = None
        self.yaw_detector = YawDetection()     # yaw angle
        # Creates a tag in the database and saves the id of the drone objects entity
        self.database_id = database.tag.put(TagModel())
        self.db_object = database.tag.get(self.database_id)  # The entity - easy read and write
        self.tag.setup()  # Setup the Tag

    def updatePosition(self):
        self.position = self.tag.getPosition()
        self.euler = self.tag.getEulerAngle()
        if self.yaw_detector.initVideocapture():
            self.yaw_detector.getAngle()

    def savePositionToDatabase(self):
        self.db_object.setPosition(self.position.x, self.position.y, self.position.z)
