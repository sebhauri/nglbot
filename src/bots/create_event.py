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
    START = 0
    DATE = 1
    LOCATION = 2
    VALIDATION = 3
    GUESTLIST = 4

TOKEN = '1361340482:AAHtu5hD-tgRrOROx8K_k6R0I015UlBNRQQ'

# Entry point of the conversation 
def start(update: Update, context: CallbackContext) -> State:
    if update.effective_chat.type == 'private':
        button = [["Yes !", "No :("]]
        update.effective_message.reply_text(
            "Welcome ! Would you like to create an event ?", reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
        )
        return State.START

# Error handler: exit the conversation
def error_response(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Something went wrong, please start over with /start")
    return ConversationHandler.END


def start_response(update: Update, context: CallbackContext) -> State:
    if  update.effective_message.text == 'No :(':
        update.message.reply_text("Sorry to see you go :(")
        return ConversationHandler.END
    elif update.effective_message.text == 'Yes !':
        context.user_data['dates'] = []
        context.user_data['location'] = []
        context.user_data['is_unique_date'] = 0
        update.message.reply_text("Propose a date (format : dd/mm/yyyy)")
        return State.DATE

def date_response(update: Update, context: CallbackContext) -> State:
    if update.effective_message.text == "Done" and context.user_data['dates']:
        update.message.reply_text("You may now want to chose a location for your event, just type it for me...")
        return State.LOCATION
    else:
        try:
            text = update.effective_message.text
            date = datetime.datetime.strptime(text, '%d/%m/%Y')
            context.user_data['dates'].append(date)
            update.message.reply_text("Type a new date if you want to add another one or type \"Done\" to go to the next step")
            context.user_data['is_unique_date'] += 1
            return State.DATE
        except ValueError as _:
            update.message.reply_text("Please... use the format dd/mm/yyyy to give me a date !")
            return State.DATE


def location_response(update: Update, context: CallbackContext) -> State:
    location = update.effective_message.text
    context.user_data['location'].append(location)
    button = [["Continue", "Abort"]]
    update.message.reply_text("Ok, here is a little recap for you : \n Your event is name : \n The date of your event is (are) : {}\n The location of your event is :{}".format(context.user_data['dates'], context.user_data['location']))
    update.message.reply_text("Are you sure you want to continue ?", reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True))
    return State.VALIDATION

def validation_response(update: Update, context: CallbackContext) -> State:
    if update.effective_message.text == 'Continue':
        return State.GUESTLIST
    elif update.effective_message.text == 'Abort':
        update.message.reply_text("OK, see you xoxo !")
        return ConversationHandler.END


def kick_off(update: Update, context: CallbackContext) -> None:
    if update.effective_chat.type != 'group':
        return
    else:
        

def main() -> None:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(ConversationHandler([CommandHandler('start', start)], {  
        State.START : [MessageHandler(Filters.text, start_response)],
        State.DATE : [MessageHandler(Filters.text, date_response)],
        State.LOCATION : [MessageHandler(Filters.text, location_response)],
        State.VALIDATION : [MessageHandler(Filters.text, validation_response)]
        } , [MessageHandler(Filters.text, error_response)]))


    # START/STOP
    updater.start_polling()
    updater.idle()