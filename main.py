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

    # creates the drone object
    drone = Drone(anchors, db)
    drone.startUpdateLoop()
