import objectbox

from models.objectbox_models import Led

model = objectbox.Model()
model.entity(Led, last_property_id=objectbox.model.IdUid(4, 3004))
model.last_entity_id = objectbox.model.IdUid(3, 3)
