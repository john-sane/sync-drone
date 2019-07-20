import objectbox
from models.objectbox_models import Led

# initialize an empty DB before the first server start the server
model = objectbox.Model()
model.entity(Led, last_property_id=objectbox.model.IdUid(3, 3004))
model.last_entity_id = objectbox.model.IdUid(3, 3)
model = objectbox.Builder().model(model).directory("led-server-db").build()