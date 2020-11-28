import logging
import bots.create_event
import bots.init_group

from telegram.ext import Updater

TOKEN = '1432985981:AAHxLzTlnqVH8uo20PPuhDFSqbWqp6hBlJw'

def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    bots.create_event.register(dispatcher)
    bots.init_group.register(dispatcher)

    # START/STOP
    updater.start_polling()
    updater.idle()