from models.objectbox_models import Led as LedModel


class Led:
    def __init__(self, database, stick_pos):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.stick_pos = stick_pos
        #self.db_id = database.led.put(LedModel())
        #self.led_object = database.led.get(self.db_id)
