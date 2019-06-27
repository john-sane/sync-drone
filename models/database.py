import objectbox
from models.objectbox_models import Anchor, Tag, Led

# Class for easy Database setups
class Database:
    def __init__(self):
        self.model = objectbox.Model()
        # loads Anchor class params
        self.anchor_entity = self.model.entity(Anchor, last_property_id=objectbox.model.IdUid(8, 1008))
        # loads Tag class params
        self.tag_entity = self.model.entity(Tag, last_property_id=objectbox.model.IdUid(8, 2008))
        # loads LED class params
        self.led_entity = self.model.entity(Led, last_property_id=objectbox.model.IdUid(5, 3005))
        # defines number of entities
        self.model.last_entity_id = objectbox.model.IdUid(3, 3)
        # the Box, where you can put Tag Objects in
        self.tag = objectbox.Box(objectbox.Builder().model(self.model).directory("db-tag").build(), Tag)
        #self.led = objectbox.Box(objectbox.Builder().model(self.model).directory("db-led").build(), Led)  # The Box, where you can put Led Objects in
