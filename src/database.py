import os
from pony.orm import *

db = Database()

def connect(create=False):
  # start a database from scratch
  if create:
    os.remove("development.sqlite")
  db.bind(provider='sqlite', filename='development.sqlite', create_db=create)
  db.generate_mapping(create_tables=create)
