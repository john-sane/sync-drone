import objectbox
import os
from time import sleep
from models.objectbox_models import Tag, Led

# class for easy Database setups
class Database:
    def __init__(self, isMaster):
        self.TagModel = objectbox.Model()
        self.LedModel = objectbox.Model()

        # load entities with last property entry
        # self.anchor_entity = self.model.entity(Anchor, last_property_id=objectbox.model.IdUid(8, 1008))
        self.tag_entity = self.TagModel.entity(Tag, last_property_id=objectbox.model.IdUid(8, 2008))
        self.led_entity = self.LedModel.entity(Led, last_property_id=objectbox.model.IdUid(4, 3004))

        # define number of entities
        self.TagModel.last_entity_id = objectbox.model.IdUid(3, 3)
        self.LedModel.last_entity_id = objectbox.model.IdUid(3, 3)

        sync_uri = "ws://192.168.43.63:9999"
        # initialize an empty DB before the first server start the server
        if isMaster is True:
            sync_uri = "ws://127.0.0.1:9999"
            sleep(1)
            os.popen('sudo ./sync-server-armv7l --unsecure-no-authentication -d server-led-db -b ws://0.0.0.0:9999')
            sleep(2)

        # the Box, where you can put Tag / Led objects in
        self.tag = objectbox.Box(objectbox.Builder().model(self.TagModel).directory("tag-db").build(), Tag)
        self.led = objectbox.Box(objectbox.Builder().model(self.LedModel).sync_uri(sync_uri)
                                 .directory("led-db").build(), Led)
