from models.drone import Drone
from models.anchor import Anchor
from models.database import Database

from time import sleep


if __name__ == "__main__":

    isMaster = True
    # define Anchor Positions (Anchor ID, Position.xyz)
    anchors = [Anchor(0x6141, [0, 0, 0]).getAnchorCoordinates(),
               Anchor(0x6674, [1100, 0, 500]).getAnchorCoordinates(),
               Anchor(0x6976, [0, 2010, 1000]).getAnchorCoordinates(),
               Anchor(0x671f, [1200, 2020, 1500]).getAnchorCoordinates()]

    # creates objectbox database
    db = Database(isMaster)

    # creates the drone object
    drone = Drone(anchors, db, isMaster)
    #drone.startUpdateLoop()
