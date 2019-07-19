from time import sleep
import random
from pypozyx import PozyxSerial, get_first_pozyx_serial_port, PozyxConstants, version, SingleRegister, Coordinates, \
    DeviceList, EulerAngles, POZYX_SUCCESS


class Tag:
    def __init__(self, anchors):
        self.serial = PozyxSerial(self.getSerialport)
        self.anchors = anchors

        # position calculation algorithm and tracking dimension
        self.algorithm = PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY
        self.dimension = PozyxConstants.DIMENSION_3D

    def setup(self):
        # sets up the Pozyx for positioning by calibrating its anchor list
        print("")
        print("POZYX POSITIONING Version {}".format(version))
        print("-------------------------------------------------------")
        print("")
        print("- System will manually configure tag")
        print("")
        print("- System will auto start positioning")
        print("")
        print("-------------------------------------------------------")
        print("")
        self.setAnchors()
        self.printConfig()
        print("")
        print("-------------------------------------------------------")
        print("")

    def setAnchors(self):
        # adds the manually measured anchors to the Pozyx's device list one for one
        status = self.serial.clearDevices(remote_id=None)
        for anchor in self.anchors:
            status &= self.serial.addDevice(anchor, remote_id=None)
        if len(self.anchors) > 4:
            status &= self.serial.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO,
                                                        len(self.anchors),
                                                        remote_id=None)

    @property
    def getSerialport(self):
        # serialport connection test
        serial_port = get_first_pozyx_serial_port()
        if serial_port is None:
            print("No Pozyx connected. Check your USB cable or your driver!")
            return None
        else:
            return serial_port

    def getPosition(self):
        # performs positioning and exports the results
        position = Coordinates()
        try:
            status = self.serial.doPositioning(position, self.dimension, self.algorithm, remote_id=None)
            if status == POZYX_SUCCESS:
                # print("POZYX data:", position)
                return position
            else:
                self.printError("positioning")
        except:
            self.printError("positioning")
            return None

    def getOrientation(self):
        # reads euler angles (yaw, roll, pitch) and exports the results
        orientation = EulerAngles()
        status = self.serial.getEulerAngles_deg(orientation)
        if status == POZYX_SUCCESS:
            # print("POZYX data:", orientation)
            return orientation
        else:
            print("Sensor data not found")
            return None

    @classmethod
    def mockedPosition(cls):
        # return Coordinates(random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000))
        return Coordinates(random.randint(0, 2000), random.randint(0, 2000), random.randint(0, 2000))

    @classmethod
    def mockedOrientation(cls):
        return EulerAngles(random.randint(0, 30), random.randint(0, 30), random.randint(0, 30))

    def printConfig(self):
        # prints the anchor configuration result
        list_size = SingleRegister()

        # prints the anchors list size
        self.serial.getDeviceListSize(list_size, None)

        if list_size[0] != len(self.anchors):
            self.printError("configuration")
            return

        # prints the anchors list
        device_list = DeviceList(list_size=list_size[0])
        self.serial.getDeviceIds(device_list, None)

        print("Calibration result:")
        print("Anchors found: {0}".format(list_size[0]))
        print("Anchor IDs: ", device_list)

        for i in range(list_size[0]):
            anchor_coordinates = Coordinates()
            self.serial.getDeviceCoordinates(device_list[i], anchor_coordinates, None)
            print("ANCHOR: 0x%0.4x, %s" % (device_list[i], str(anchor_coordinates)))
            sleep(0.025)

    def printError(self, operation):
        # Prints Pozyx's errors
        error_code = SingleRegister()
        if None is None:
            self.serial.getErrorCode(error_code)
            print("LOCAL ERROR %s, %s" % (operation, self.serial.getErrorMessage(error_code)))
            return
        status = self.serial.getErrorCode(error_code, None)
        if status == POZYX_SUCCESS:
            print("ERROR %s on ID %s, %s" %
                  (operation, "0x%0.4x" % None, self.serial.getErrorMessage(error_code)))
        else:
            self.serial.getErrorCode(error_code)
            print("ERROR %s, couldn't retrieve remote error code, LOCAL ERROR %s" %
                  (operation, self.serial.getErrorMessage(error_code)))
