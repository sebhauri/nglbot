from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    Filters,
    CallbackContext,
    Dispatcher
)

from telegram import (
    ReplyKeyboardMarkup,
    Update,
)

from enum import Enum

import logging
import datetime

class State(Enum):
    START = 0

def group_start(update: Update, context: CallbackContext) -> State:
    if update.effective_chat.type == 'group':
        # create poll based on received event ID
        event_id = update.effective_message.text.split(" ")[1]

        update.effective_message.reply_text(f"Starting setup of event with id {event_id}")

        # TODO query infos about event
        pass
    else:
        update.message.reply_text("This command can only be issued in a group")

def register(dispatcher: Dispatcher):
    dispatcher.add_handler(ConversationHandler([CommandHandler('groupstart', group_start)], {}, []))
