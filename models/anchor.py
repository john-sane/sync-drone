from pypozyx import Coordinates, DeviceCoordinates


class Anchor:
    def __init__(self, anchor_id, coordinates):
        self.anchor_id = anchor_id  # Anchor ID / Written on the side of each anchor case
        self.type = 1               # Type: 0 = Tag, 1 = Anchor
        # coordinates = Position of Anchor in the room (Values from the setup program)
        self.coordinates = Coordinates(coordinates[0], coordinates[1], coordinates[2])

    def getAnchorCoordinates(self):
        return DeviceCoordinates(self.anchor_id, self.type, self.coordinates)
