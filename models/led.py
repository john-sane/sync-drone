from models.objectbox_models import Led as LedModel


class Led:
    def __init__(self, database, tag_id, arm_nr, stick_pos):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.tag_id = tag_id
        self.arm_nr = arm_nr
        self.stick_pos = stick_pos
        self.db_id = database.led.put(LedModel())
        self.led_object = database.led.get(self.db_id)
