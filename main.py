from models.drone import Drone
from models.anchor import Anchor
from models.database import Database

from time import sleep


if __name__ == "__main__":

    # define Anchor Positions (Anchor ID, Position.xyz)
    anchors = [Anchor(0x6674, [2400, 4200, 0]).getAnchorCoordinates(),
               Anchor(0x6976, [0, 4200, 0]).getAnchorCoordinates(),
               Anchor(0x6141, [0, 0, 0]).getAnchorCoordinates(),
               Anchor(0x671f, [1800, 1600, 0]).getAnchorCoordinates()]

    # creates objectbox database
    db = Database()

    # creates the drone object
    drone = Drone(anchors, db)
    drone.startUpdateLoop()
