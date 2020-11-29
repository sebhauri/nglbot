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

def group_start(update: Update, context: CallbackContext) -> State:
    if update.effective_chat.type == 'group':
        # create poll based on received event ID
        words = update.effective_message.text.split(' ')

        if len(words) <= 1:
            update.message.reply_text('Please specify the event ID')
        else:
            event_uuid = words[1]
            event = query_event(event_uuid)


            if event == None:
                update.message.reply_text(f"Event with ID {event_uuid} does not exist\nPlease try again")
                return None

            context.chat_data['event_id'] = event.id
            
            update.message.reply_text(f'Starting setup of event with id {event_uuid}')

            poll = query_poll(event)
            event_dates = poll.options

            message: Message = context.bot.send_poll(
                update.effective_chat.id,
                "Are you available at the following dates?",
                event_dates,
                is_anonymous=False,
                allows_multiple_answers=True,
            )

            update.effective_user.send_message("Here is the poll for your event")
            message.forward(update.effective_user.id)

            options = [event_dates]
            update.effective_user.send_message("Have you made your choice for the date ?", reply_markup=ReplyKeyboardMarkup(options, one_time_keyboard=True))
            
            return State.VOTING
        pass
    else:
        update.message.reply_text('This command can only be issued in a group')

def close_poll(update: Update, context: CallbackContext) -> State:
    if update.effective_chat.type == 'group':
        button = [["I'm in !", "I'm out !"]]
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

@orm.db_session
def query_event(event_uuid: str) -> Event:
    return Event.get(uuid=event_uuid)

@orm.db_session
def query_poll(event: Event) -> Poll:
    return Poll.get(event=event.id) # TODO filtering on event might not be sufficient

def register(dispatcher: Dispatcher):
    dispatcher.add_handler(ConversationHandler([CommandHandler('groupstart', group_start)], {
        State.VOTING : [CommandHandler('kick', close_poll)],
        State.CONFIRMING : [MessageHandler(Filters.text & (~Filters.command), kick)]
    }, []))
