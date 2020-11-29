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
    Message
)

from enum import Enum
from pony import orm

from models.event import Event
from models.poll import Poll
from models.guest import Guest

import logging
import datetime

class State(Enum):
    START = 0
    VOTING = 1
    CONFIRMING = 2

@orm.db_session
def group_start(update: Update, context: CallbackContext) -> State:
    if update.effective_chat.type == 'group':
        # create poll based on received event ID
        words = update.effective_message.text.split(' ')

        if len(words) <= 1:
            update.message.reply_text('Please specify the event ID')
        else:
            event_uuid = words[1]
            event = Event.get(uuid=event_uuid)

            if event == None:
                update.message.reply_text(f"Event with ID {event_uuid} does not exist\nPlease try again")
                return None

            context.chat_data['event_id'] = event.id
            
            poll = Poll.get(event=event.id)
            event_dates = poll.options

            if len(event_dates) == 1:
                update.message.reply_text(f'Hi everybody ! You have been invited to the event {event.name} which will take place on the {event.date}.\n The location is : {event.location}. \n\n Have a nice event !!!')
            else:
                message: Message = context.bot.send_poll(
                    update.effective_chat.id,
                    f"Hi everybody ! You have been invited to the event {event.name} which will take place at : {event.location}.\n\nPlease answer the following poll with your availability so that the date can be chosen.",
                    event_dates,
                    is_anonymous=False,
                    allows_multiple_answers=True,
                )

                update.effective_user.send_message("Here is the poll for your event")
                message.forward(update.effective_user.id)

                options = [event_dates]
                update.effective_user.send_message("Have you made your choice for the date ?", reply_markup=ReplyKeyboardMarkup(options, one_time_keyboard=True))
            
            return State.VOTING
    else:
        update.message.reply_text('This command can only be issued in a group')

@orm.db_session
def close_poll(update: Update, context: CallbackContext) -> State:
    if update.effective_chat.type == 'group':
        button = [["I'm in !", "I'm out !"]]
        event = Event[context.chat_data['event_id']]
        update.message.reply_text(f"The event takes place on the {event.date}")
        update.message.reply_text("Will you be in this event ?", reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True))
        return State.CONFIRMING

@orm.db_session
def kick(update: Update, context: CallbackContext) -> None:
    if update.message.text == "I'm out !":
        update.effective_chat.kick_member(user_id=update.message.from_user.id)
    elif update.message.text == "I'm in !":
        user_id = update.message.from_user.id
        event_id = context.chat_data['event_id']
        username = update.effective_user.username
        event = Event[event_id]
        event.guests.add(Guest(uuid=user_id, event=event, username=username))

def register(dispatcher: Dispatcher):
    dispatcher.add_handler(ConversationHandler([CommandHandler('groupstart', group_start)], {
        State.VOTING : [CommandHandler('kick', close_poll)],
        State.CONFIRMING : [MessageHandler(Filters.text & (~Filters.command), kick)]
    }, []))
