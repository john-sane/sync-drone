import objectbox
from models.objectbox_models import Anchor, Tag

# Class for easy Database setups
class Database:
    def __init__(self):
        self.model = objectbox.Model()
        self.anchor_entity = self.model.entity(Anchor, last_property_id=objectbox.model.IdUid(8, 1008))
        self.tag_entity = self.model.entity(Tag, last_property_id=objectbox.model.IdUid(23, 2023))
        self.tag_box = None  # The Box, where you can put Tag Objects in

        def setup_models(model):
            self.model.last_entity_id = objectbox.model.IdUid(2, 2)
            self.tag_box = objectbox.Box(objectbox.Builder().model(self.model).directory("db").build(), model)

        setup_models(Tag)
