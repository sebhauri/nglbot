import os
from pony.orm import *

db = Database()

DB_FILENAME = "development.sqlite"

def connect(create=False):
  # start a database from scratch
  if create and os.path.isfile(DB_FILENAME):
      os.remove(DB_FILENAME)
    
  db.bind(provider='sqlite', filename='development.sqlite', create_db=create)
  db.generate_mapping(create_tables=create)
