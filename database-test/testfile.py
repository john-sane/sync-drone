import objectbox
from mytestpackage.model import Anchor, Tag

# Configure ObjectBox - should be done only once in the whole program and the "ob" variable should be kept around
model = objectbox.Model()
model.entity(Anchor, last_property_id=objectbox.model.IdUid(8, 1008))
model.entity(Tag, last_property_id=objectbox.model.IdUid(23, 2023))
model.last_entity_id = objectbox.model.IdUid(2, 2)
ob = objectbox.Builder().model(model).directory("db").build()

# Open the box of "Person" entity. This can be called many times but you can also pass the variable around
box = objectbox.Box(ob, Anchor)

id = box.put(Anchor())  # Create
anchorObject = box.get(id)  # Read

# test data anchor
anchorObject.anchor_name = "0x61f1"
anchorObject.getAnchorname()
anchorObject.pos_x = 150
anchorObject.pos_y = 200
anchorObject.pos_z = 100
anchorObject.getPosition()
anchorObject.latency = 2.1
anchorObject.update_rate = 52.89
anchorObject.success_rate = 52.89
anchorObject.getMetrics()

box.put(anchorObject)  # Update
box.remove(anchorObject)  # Delete

box = objectbox.Box(ob, Tag)

id = box.put(Tag())  # Create
tagObject = box.get(id)  # Read

# test data tag
tagObject.tag_name = "0x45f67"
tagObject.getTagname()
tagObject.pos_x = 320
tagObject.pos_y = 100
tagObject.pos_z = 240
tagObject.getPosition()
tagObject.pos_x = 1
tagObject.pos_y = 2
tagObject.pos_z = 3
tagObject.getAcceleration()
tagObject.mag_x = 4
tagObject.mag_y = 5
tagObject.mag_z = 6
tagObject.getMagneticField()
tagObject.yaw = 30
tagObject.roll = 40
tagObject.pitch = 50
tagObject.getOrientation()
tagObject.ang_velo_x = 30
tagObject.ang_velo_y = 40
tagObject.ang_velo_z = 50
tagObject.getAngularVelocity()
tagObject.grav_x = 30
tagObject.grav_y = 40
tagObject.grav_z = 50
tagObject.getGravityVector()

box.put(tagObject)  # Update
box.remove(tagObject)  # Delete