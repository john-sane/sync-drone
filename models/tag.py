from time import sleep

from pypozyx import PozyxSerial, get_first_pozyx_serial_port, PozyxConstants, version, SingleRegister, Coordinates, \
    DeviceList, EulerAngles, POZYX_SUCCESS


class Tag:
    def __init__(self, anchors):
        self.serial = PozyxSerial(self.getSerialport())
        self.anchors = anchors

        # position calculation algorithm and tracking dimension
        self.algorithm = PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY
        self.dimension = PozyxConstants.DIMENSION_3D

    def setup(self):
        # Sets up the Pozyx for positioning by calibrating its anchor list
        print("")
        print("------------POZYX POSITIONING Version{} -------------".format(version))
        print("")
        print("- System will manually configure tag")
        print("")
        print("- System will auto start positioning")
        print("")
        print("---------------------------------------------------")
        print("")
        self.setAnchors()
        self.printConfig()
        print("")
        print("---------------------------------------------------")

    def setAnchors(self):
        # Adds the manually measured anchors to the Pozyx's device list one for one
        status = self.serial.clearDevices(remote_id=None)
        for anchor in self.anchors:
            status &= self.serial.addDevice(anchor, remote_id=None)
        if len(self.anchors) > 4:
            print('All here')
            status &= self.serial.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO,
                                                        len(self.anchors),
                                                        remote_id=None)

    def getSerialport(self):
        # serialport connection test
        serial_port = get_first_pozyx_serial_port()
        if serial_port is None:
            print("No Pozyx connected. Check your USB cable or your driver!")
            quit()
        else:
            return serial_port

    def getPosition(self):
        # performs positioning and exports the results
        position = Coordinates()
        status = self.serial.doPositioning(
            position, self.dimension, self.algorithm, remote_id=None)
        if status == POZYX_SUCCESS:
            return position
        else:
            self.printError("positioning")

    def getEulerAngle(self):
        # reads euler angles (heading, roll, pitch) and exports the results
        euler_angles = EulerAngles()
        self.serial.getEulerAngles_deg(euler_angles)
        print("---- ORIENTATION (degree) ----")
        print(euler_angles)
        return euler_angles

    def printConfig(self):
        # prints the anchor configuration result
        list_size = SingleRegister()

        self.serial.getDeviceListSize(list_size, None)
        print("List size: {0}".format(list_size[0]))

        if list_size[0] != len(self.anchors):
            self.printError("configuration")
            return

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
        # Prints the Pozyx's error
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
