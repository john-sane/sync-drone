import objectbox
from models.objectbox_models import Anchor, Tag

# Class for easy Database setups
class Database:
    def __init__(self):
        self.model = objectbox.Model()
        self.anchor_entity = self.model.entity(Anchor, last_property_id=objectbox.model.IdUid(8, 1008))
        self.tag_entity = self.model.entity(Tag, last_property_id=objectbox.model.IdUid(8, 2008)) # loads Tag class params
        self.led_entity = self.model.entity(Led, last_property_id=objectbox.model.IdUid(5, 3005)) # loads LED class params
        self.model.last_entity_id = objectbox.model.IdUid(3, 3)
        self.tag = objectbox.Box(objectbox.Builder().model(self.model).directory("db").build(), Tag)  # The Box, where you can put Tag Objects in
        self.led = objectbox.Box(objectbox.Builder().model(self.model).directory("db").build(), Led)  # The Box, where you can put Led Objects in
