from models.drone import Drone
from models.anchor import Anchor
from models.database import Database

from time import sleep


if __name__ == "__main__":

    # define Anchor Positions (Anchor ID, Position.xyz)
    anchors = [Anchor(0x6674, [4139, 594, 2000]).getAnchorCoordinates(),
               Anchor(0x6976, [-768, 4320, 1200]).getAnchorCoordinates(),
               Anchor(0x6141, [-749, 750, 1300]).getAnchorCoordinates(),
               Anchor(0x671f, [-2229, 3645, 1000]).getAnchorCoordinates()]

    # creates objectbox database
    db = Database()

    # create the drone object
    drone = Drone(anchors, db)

    while True:
        # update the current position of the drone every 0.1 seconds and print it
        drone.updatePosition()
        sleep(0.1)
        if drone.position is not None:
            drone.savePositionToDatabase()
            drone.db_object.getPosition()
    else:
        pass
