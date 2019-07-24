from models.drone import Drone
from models.anchor import Anchor
from models.database import Database

from time import sleep


if __name__ == "__main__":

    isMaster = True
    # define Anchor Positions (Anchor ID, Position.xyz)
    anchors = [Anchor(0x6141, [3230, 0, 20]).getAnchorCoordinates(),
               Anchor(0x6674, [0, 2840, 1080]).getAnchorCoordinates(),
               Anchor(0x6976, [0, 0, 1400]).getAnchorCoordinates(),
               Anchor(0x671f, [3230, 1610, 1120]).getAnchorCoordinates(),
               Anchor(0x6a41, [0, 2240, 915]).getAnchorCoordinates()]

    # creates objectbox database
    db = Database(isMaster)

    # creates the drone object
    drone = Drone(anchors, db, isMaster)
    drone.startUpdateLoop()
