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
from pony import orm

from models.event import Event
from models.poll import Poll

import logging
import datetime

class State(Enum):
    START = 0
    VOTING = 1

def group_start(update: Update, context: CallbackContext) -> State:
    if update.effective_chat.type == 'group':
        # create poll based on received event ID
        words = update.effective_message.text.split(' ')

        if len(words) <= 1:
            update.message.reply_text('Please specify the event ID')
        else:
            event_uuid = words[1]
            event = query_event(event_uuid)

            context.chat_data['event_id'] = event.id

            if event == None:
                update.message.reply_text(f"Event with ID {event_uuid} does not exist\nPlease try again")
                return None
            
            update.message.reply_text(f'Starting setup of event with id {event_uuid}')

            poll = query_poll(event)
            event_dates = poll.options

            message = context.bot.send_poll(
                update.effective_chat.id,
                "Are you available at the following dates?",
                event_dates,
                is_anonymous=False,
                allows_multiple_answers=True,
            )
            # TODO is this necessary ?
            # payload = {
            #     message.poll.id: {
            #         "questions": event_dates,
            #         "message_id": message.message_id,
            #         "chat_id": update.effective_chat.id,
            #         "answers": 0,
            #     }
            # }

            # TODO poll id should probably be stored on DB
            # context.bot_data.update(payload)
            return State.VOTING
        pass
    else:
        update.message.reply_text('This command can only be issued in a group')

def close_poll(update: Update, context: CallbackContext) -> State:
    pass

@orm.db_session
def query_event(event_uuid: str) -> Event:
    return Event.get(uuid=event_uuid)

@orm.db_session
def query_poll(event: Event) -> Poll:
    return Poll.get(event=event.id) # TODO filtering on event might not be sufficient

def register(dispatcher: Dispatcher):
    dispatcher.add_handler(ConversationHandler([CommandHandler('groupstart', group_start)], {
        State.VOTING : [CommandHandler('closepoll', close_poll)],
    }, []))
