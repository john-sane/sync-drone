from objectbox.model import *


@Entity(id=1, uid=1)
class Anchor:

    id = Id(id=1, uid=1001)
    anchor_name = Property(str, id=2, uid=1002)
    pos_x = Property(int, id=3, uid=1003)
    pos_y = Property(int, id=4, uid=1004)
    pos_z = Property(int, id=5, uid=1005)
    latency = Property(float, id=6, uid=1006)
    update_rate = Property(float, id=7, uid=1007)
    success_rate = Property(float, id=8, uid=1008)

    def setAnchorname(self):
        self.anchor_name = "0x61f1"

    def printAnchorname(self):
        print('Anchor:', self.anchor_name)

    def setPosition(self, x, y, z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z

    def printPosition(self):
        print("POSITION: X: {p.pos_x} Y: {p.pos_y} Z: {p.pos_z}".format(p=self))

    """def setMetrics(self):
        self.latency = 2.1
        self.update_rate = 52.89
        self.success_rate = 52.89

    def getMetrics(self):
        print('Latency:', self.latency)
        print('Update Rate:', self.update_rate)
        print('Success Rate:', self.success_rate)"""


@Entity(id=2, uid=2)
class Tag:

    id = Id(id=1, uid=2001)
    tag_name = Property(str, id=2, uid=2002)
    pos_x = Property(int, id=3, uid=2003)
    pos_y = Property(int, id=4, uid=2004)
    pos_z = Property(int, id=5, uid=2005)
    yaw = Property(int, id=6, uid=2006)
    roll = Property(int, id=7, uid=2007)
    pitch = Property(int, id=8, uid=2008)

    def setTagname(self):
        self.tag_name = "0x45f67"

    def printTagname(self):
        print('Tag:', self.tag_name)

    def setPosition(self, x, y, z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z

    def printPosition(self):
        print("DATABASE:")
        print("X: {p.pos_x} Y: {p.pos_y} Z: {p.pos_z}".format(p=self))
        print("")

    def setOrientation(self, yaw, roll, pitch):
        self.yaw = yaw
        self.roll = roll
        self.pitch = pitch

    def printOrientation(self):
        print("DATABASE:")
        print("yaw: {p.yaw} roll: {p.roll} pitch: {p.pitch}".format(p=self))
        print("")