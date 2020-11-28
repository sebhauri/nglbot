from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    Filters,
    CallbackContext,
)

from telegram import (
    ReplyKeyboardMarkup,
    Update,
)

from enum import Enum

import logging
import datetime

class State(Enum):
    SLEEP = 0
    START = 1
    DATE = 2
    DATE_BIS = 3
    LOCATION = 4

TOKEN = '1432985981:AAHxLzTlnqVH8uo20PPuhDFSqbWqp6hBlJw'

def start(update: Update, context: CallbackContext) -> State:
    button = [["Yes !", "No :("]]
    update.effective_message.reply_text(
        "Welcome ! Would you like to creat an event ?", reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
    )
    return State.START

def error_response(update: Update, context: CallbackContext) -> State:
    update.message.reply_text("Something went wrong, please start over with /start")

def sleep_response(update: Update, context: CallbackContext) -> State:
    update.message.reply_text("Use /start to start planning an event")
    return State.START

def start_response(update: Update, context: CallbackContext) -> State:
    if  update.effective_message.text == 'No :(':
        update.message.reply_text("Sorry to see you go :(")
        return State.SLEEP
    elif update.effective_message.text == 'Yes !':
        update.message.reply_text("Propose a date (format : dd/mm)")
        return State.DATE

def date_response(update: Update, context: CallbackContext) -> State:
    update.message.reply_text("Type a new date if you want to add another one or type \"Done\" to go to the next step")
    return State.DATE_BIS

def date_bis_response(update : Update, context : CallbackContext) ->State:
    if update.effective_message.text == 'Done':
        update.replay_text("You may now want to chose a location for your event, just type it for me...")
        return State.LOCATION
    else:
        text = update.effective_message.text
        try:
            date = datetime.datetime.strotime(text, '%d.%m.%Y')
            # TODO save date
        except ValueError as error:
            # handle error
            pass

        return State.DATE_BIS

def location_response(update: Update, context: CallbackContext) ->State:
    ...



def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    #Commands handlers
    dispatcher.add_handler(ConversationHandler([CommandHandler('start', start)], {  
        State.SLEEP : [MessageHandler(Filters.text & (~Filters.command), sleep_response)],
        State.START : [MessageHandler(Filters.text, start_response)],
        State.DATE : [MessageHandler(Filters.text, date_response)],
        State.DATE_BIS : [MessageHandler(Filters.text, date_bis_response)],
        State.LOCATION : [MessageHandler(Filters.text, location_response)]
        } , [MessageHandler(Filters.text, error_response)]))


    #START/STOP
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()