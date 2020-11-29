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
import uuid

from pony.orm import *
from models.event import Event
from models.poll import Poll

class State(Enum):
    START = 0
    NAME = 1
    DATE = 2
    LOCATION = 3
    VALIDATION = 4
    GUESTLIST = 5

# Entry point of the conversation 
def start(update: Update, context: CallbackContext) -> State:
    if update.effective_chat.type == 'private':
        button = [["Yes !", "No :("]]
        update.message.reply_text(
            "Welcome ! Would you like to create an event ?", reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
        )
        return State.START

# Cancel
def cancel(update: Update, context: CallbackContext) -> State:
    update.message.reply_text("Sorry to see you leave :'(\nStart an event with /start")
    return ConversationHandler.END

# Error handler: exit the conversation
def error_response(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Something went wrong, please start over with /start")
    return ConversationHandler.END

# START
def start_response(update: Update, context: CallbackContext) -> State:
    if  update.effective_message.text == 'No :(':
        update.message.reply_text("Sorry to see you go :(")
        return ConversationHandler.END
    elif update.effective_message.text == 'Yes !':
        update.message.reply_text("Good. What's the name of your event ?")
        return State.NAME

# NAME
def name_response(update: Update, context: CallbackContext) -> State:
    name = update.effective_message.text
    context.user_data['uuid'] = update.effective_user.id
    context.user_data['name'] = name
    context.user_data['dates'] = []
    update.message.reply_text("Propose a date (format : dd.mm.yyyy)")
    return State.DATE

# DATE
def date_response(update: Update, context: CallbackContext) -> State:
    if update.effective_message.text == "Done" and context.user_data['dates']:
        update.message.reply_text("You may now want to chose a location for your event, just type it for me...")
        return State.LOCATION
    else:
        try:
            text = update.effective_message.text
            date = datetime.datetime.strptime(text, '%d.%m.%Y')
            context.user_data['dates'].append(date)
            button = [["Done"]]
            update.message.reply_text("Type a new date if you want to add another one or press \"Done\" to go to the next step", reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True))
            return State.DATE
        except ValueError as _:
            update.message.reply_text("Please... use the format dd.mm.yyyy to give me a date !")
            return State.DATE

# LOCATION
def location_response(update: Update, context: CallbackContext) -> State:
    location = update.effective_message.text
    context.user_data['location'] = location
    button = [["Continue", "Abort"]]
    summary = "Ok, here is a little recap for you:\n"
    summary += f"Your event's name is {context.user_data['name']}\n"
    summary += f"Your location is {context.user_data['location']}\n"
    summary += "Your dates are:\n"
    for date in context.user_data['dates']: summary += f"- {date.strftime('%d %b %Y')}\n"
    update.message.reply_text(summary + "\nAre you sur you want to continue ?", reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True))
    return State.VALIDATION

# VALIDATION: abort or commit the event
@db_session
def validation_response(update: Update, context: CallbackContext) -> State:
    if update.effective_message.text == 'Continue':
        # save the event to the database
        dates = [date.strftime("%d %b %Y") for date in context.user_data['dates']]
        event = Event(name = context.user_data['name'], uuid=uuid.uuid4().hex, user_uuid=context.user_data['uuid'])
        poll = Poll(type=Poll.TYPES['dates'], question="Select the dates you are available", event=event, options=dates)
        commit()

        message = "Your event has been created. You may now create a group. "\
            "The guests as well as this bot should be added to the group. "\
            "After that, forward the following message to the newly created group."
        update.message.reply_text(message)
        update.message.reply_text(f"/groupstart {event.uuid}")
        return State.GUESTLIST
    elif update.effective_message.text == 'Abort':
        update.message.reply_text("OK, see you xoxo !")
        return ConversationHandler.END
        

def register(dispatcher: Dispatcher):
    # Register handlers
    dispatcher.add_handler(ConversationHandler([CommandHandler('start', start)], {  
        State.START : [MessageHandler(Filters.text & (~Filters.command), start_response)],
        State.NAME : [MessageHandler(Filters.text & (~Filters.command), name_response)],
        State.DATE : [MessageHandler(Filters.text & (~Filters.command), date_response)],
        State.LOCATION : [MessageHandler(Filters.text & (~Filters.command), location_response)],
        State.VALIDATION : [MessageHandler(Filters.text & (~Filters.command), validation_response)]
        }, [CommandHandler('cancel', cancel), MessageHandler(Filters.all, error_response)]))