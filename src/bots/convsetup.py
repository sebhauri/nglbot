import logging
import bots.create_event
import bots.init_group

from telegram.ext import Updater

import yaml

with open("config/secrets.yml") as file:
    secrets = yaml.load(file, Loader=yaml.FullLoader)
    TOKEN = secrets['development']['API_TOKEN']

def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    bots.create_event.register(dispatcher)
    bots.init_group.register(dispatcher)

    # START/STOP
    updater.start_polling()
    updater.idle()