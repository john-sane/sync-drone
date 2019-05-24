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

    def getAnchorname(self):
        print('Anchor:', self.anchor_name)

    def setPosition(self, x, y, z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z

    def getPosition(self):
        print("--- POSITION --- X: {p.pos_x} Y: {p.pos_y} Z: {p.pos_z}".format(p=self))

    """def setMetrics(self):
        self.latency = 2.1
        self.update_rate = 52.89
        self.success_rate = 52.89

    def getMetrics(self):
        print('Latency:', self.latency)
        print('Update Rate:', self.update_rate)
        print('Success Rate:', self.success_rate)"""

    """def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)"""



@Entity(id=2, uid=2)
class Tag:

    id = Id(id=1, uid=2001)
    tag_name = Property(str, id=2, uid=2002)
    pos_x = Property(int, id=3, uid=2003)
    pos_y = Property(int, id=4, uid=2004)
    pos_z = Property(int, id=5, uid=2005)
    """acc_x = Property(int, id=6, uid=2006)
    acc_y = Property(int, id=7, uid=2007)
    acc_z = Property(int, id=8, uid=2008)
    lin_acc_x = Property(int, id=9, uid=2009)
    lin_acc_y = Property(int, id=10, uid=2010)
    lin_acc_z = Property(int, id=11, uid=2011)
    mag_x = Property(int, id=12, uid=2012)
    mag_y = Property(int, id=13, uid=2013)
    mag_z = Property(int, id=14, uid=2014)
    yaw = Property(int, id=15, uid=2015)
    roll = Property(int, id=16, uid=2016)
    pitch = Property(int, id=17, uid=2017)
    ang_velo_x = Property(int, id=18, uid=2018)
    ang_velo_y = Property(int, id=19, uid=2019)
    ang_velo_z = Property(int, id=20, uid=2020)
    grav_x = Property(int, id=21, uid=2021)
    grav_y = Property(int, id=22, uid=2022)
    grav_z = Property(int, id=23, uid=2023)"""

    def setTagname(self):
        self.tag_name = "0x45f67"

    def getTagname(self):
        print('Tag:', self.tag_name)

    def setPosition(self, x, y, z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z

    def getPosition(self):
        print('Position X:', self.pos_x, end = ' / ')
        print('Position Y:', self.pos_y, end = ' / ')
        print('Position Z:', self.pos_z)

    """def getAcceleration(self):
        print('Acceleration X:', self.acc_x)
        print('Acceleration Y:', self.acc_y)
        print('Acceleration Z:', self.acc_z)

    def getMagneticField(self):
        print('Magnetic Field X:', self.mag_x)
        print('Magnetic Field Y:', self.mag_y)
        print('Magnetic Field Z:', self.mag_z)

    def getOrientation(self):
        print('Yaw X:', self.yaw)
        print('Roll Y:', self.roll)
        print('Pitch Z:', self.pitch)

    def getAngularVelocity(self):
        print('Angular Velocity X:', self.ang_velo_x)
        print('Angular Velocity Y:', self.ang_velo_y)
        print('Angular Velocity Z:', self.ang_velo_z)

    def getGravityVector(self):
        print('Gravity Vector X:', self.grav_x)
        print('Gravity Vector Y:', self.grav_y)
        print('Gravity Vector Z:', self.grav_z)"""
