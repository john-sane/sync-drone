from models.objectbox_models import Led as LedModel


class Led:
    def __init__(self, database, tag_id):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.tag_id = tag_id
        self.db_id = database.led.put(LedModel())
        self.led_object = database.led.get(self.db_id)

    def saveColorToDatabase(self, database):
        self.led_object.setColor(self.red, self.green, self.blue)
        database.led.put(self.led_object)
        self.led_object.printColor()
