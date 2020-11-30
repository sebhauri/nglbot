from pony.orm import *

from database import db
from models.event import Event

class Guest(db.Entity):
  id = PrimaryKey(int, auto=True)
  uuid = Required(int)
  event = Required(Event)
  username = Optional(str)