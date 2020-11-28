from pony.orm import *

from database import db
from models.event import Event

class Poll(db.Entity):

  TYPES = {"dates": 0}

  id = PrimaryKey(int, auto=True)
  question = Required(str)
  type = Required(int)
  event = Required(Event)
  options = Optional(StrArray)