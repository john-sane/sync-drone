import objectbox
from models.objectbox_models import Anchor, Tag, Led

# class for easy Database setups
class Database:
    def __init__(self):
        self.model = objectbox.Model()

        # load entities with last property entry
        self.anchor_entity = self.model.entity(Anchor, last_property_id=objectbox.model.IdUid(8, 1008))
        self.tag_entity = self.model.entity(Tag, last_property_id=objectbox.model.IdUid(8, 2008))
        self.led_entity = self.model.entity(Led, last_property_id=objectbox.model.IdUid(5, 3005))

        # define number of entities
        self.model.last_entity_id = objectbox.model.IdUid(3, 3)

        # the Box, where you can put Tag / Led objects in
        self.tag = objectbox.Box(objectbox.Builder().model(self.model).directory("db").build(), Tag)
        #self.led = objectbox.Box(objectbox.Builder().model(self.model).directory("db").build(), Led)
