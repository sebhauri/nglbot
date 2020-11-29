from pony.orm import *

from database import db

class Event(db.Entity):

  id = PrimaryKey(int, auto=True)
  uuid = Required(str)
  name = Required(str)
  user_uuid = Required(int)
  polls = Set('Poll')
  guests = Set('Guest')
  date = Optional(str)