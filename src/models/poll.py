from pony.orm import *

from database import db
from models.event import Event

class Poll(db.Entity):

  id = PrimaryKey(int, auto=True)
  name = Required(str)
  event = Required(Event)