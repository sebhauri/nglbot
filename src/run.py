import argparse
from pony.orm import *

from database import connect
from models.event import Event
from models.poll import Poll
from models.guest import Guest

from bots.flow import main

def run():
  main()
  

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='Angelo starts his service')

  parser.add_argument('--create_db', dest='create_db', action="store_const", const=True, default=False,
                      help='Set the option to create a new database')

  args = parser.parse_args()

  connect(create=args.create_db)
  run()