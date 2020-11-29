from enum import Enum

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    Dispatcher,
    Filters
)

from telegram import (
    ReplyKeyboardMarkup,
    Update,
)

from pony.orm import *
from models.event import Event


def start(update: Update, context: CallbackContext) -> None:
    if update.effective_chat.type == 'group':
        button = [["I'm in !", "I'm out !"]]
        update.message.reply_text("Will you be in this event ?", reply_markup=ReplyKeyboardMarkup(button))

def kick(update: Update, context: CallbackContext) -> None:
    if update.message.text == "I'm out !":
        update.effective_chat.kick_member(user_id=update.message.from_user.id)
    else:
        user_id = update.message.from_user.id
        event_id = context.chat_data['event_id']
        Event[event_id].guests.add(user_id)
        

def register(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler('kick', start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), kick))
    