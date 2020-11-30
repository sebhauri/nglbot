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
    InlineQueryResultArticle
)

import requests
from enum import Enum

API_URL = "http://transport.opendata.ch/v1/"

class State(Enum):
    LOCATION = 0

# Cancel
def cancel(update: Update, context: CallbackContext) -> State:
    update.message.reply_text("Sorry to see you leave :'(\nStart an event with /start")
    return ConversationHandler.END

# Error handler: exit the conversation
def error_response(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Something went wrong, please start over with /start")
    return ConversationHandler.END

# Entry point
def timetable(update: Update, context: CallbackContext) -> None:
    update.effective_user.send_message("Please enter your location with: /location <location>")

def location(update: Update, context: CallbackContext) -> State:
    r = requests.get(API_URL + "locations", params={"query":"Vaulruz", "type":"station"}).json()
    stations = r['stations']
    if len(stations) > 1:
        answer = "Multiple stations found for your requests. Please select one"
        buttons = [[station['name']] for station in stations]
        update.message.reply_text(answer, reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True))
        return State.LOCATION

    context.user_data['location'] = stations[0]['name']
    return state.LOCATION

def connections() -> State:
    location = context.user_data['location']
    r = requests.get(API_URL + "connections", params={"from": location, "to": "Lausanne-Gare"}).json()
    connections = r['connections']
    answer = "Here are the first 5 connections:\n"
    for c in connections:
        answer += c['departure']
    update.effective_user.send_message(answer)
    return ConversationHandler.END

def register(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler('timetable', timetable))
    dispatcher.add_handler(ConversationHandler([CommandHandler('location', location)], {  
        State.LOCATION : [MessageHandler(Filters.text & (~Filters.command), location)],
    }, [CommandHandler('cancel', cancel), MessageHandler(Filters.all, error_response)]))
