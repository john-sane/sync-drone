from models.drone import Drone
from models.anchor import Anchor
from models.database import Database
from models.detection import Detection

from time import sleep
import objectbox


if __name__ == "__main__":

    # define Detection object (src = dev/video0)
    stream = Detection(0)
    stream.setup()  # stream settings
    stream.streaming()

    # define Anchor Positions (Anchor ID, Position.xyz)
    """anchors = [Anchor(0x6674, [4139, 594, 2000]).getAnchorCoordinates(),
               Anchor(0x6976, [-768, 4320, 1200]).getAnchorCoordinates(),
               Anchor(0x6141, [-749, 750, 1300]).getAnchorCoordinates(),
               Anchor(0x671f, [-2229, 3645, 1000]).getAnchorCoordinates()]
    # Creates objectbox Database and
    db = Database()

    # Create the Drone
    drone = Drone(anchors, db)

    # Update the current position of the Drone every 0.1 seconds and print it
    while True:
        drone.updatePosition()
        sleep(0.1)
        if drone.position is not None:
            drone.savePositionToDatabase()
            drone.db_object.getPosition()"""
