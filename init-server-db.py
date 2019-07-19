import objectbox
from models import model

# initialize an empty DB before the first server start the server
model = objectbox.Builder().model(model).directory("led-server-db").build()