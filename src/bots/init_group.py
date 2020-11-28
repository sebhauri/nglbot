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
    VOTING = 1

def group_start(update: Update, context: CallbackContext) -> State:
    if update.effective_chat.type == 'group':
        # create poll based on received event ID
        words = update.effective_message.text.split(' ')

        if len(words) <= 1:
            update.message.reply_text('Please specify the event ID')
        else:
            event_id = words[1]

            event = query_event(event_id)

            context.chat_data['event_info'] = event
            update.message.reply_text(f'Starting setup of event with id {event_id}')

            # TODO get actual event info
            event_dates = ['05.12.2020', '06.12.2020', '10.12.2020']
            #event_name = 'Covid party'

            message = context.bot.send_poll(
                update.effective_chat.id,
                "Are you available at the following dates?",
                event_dates,
                is_anonymous=False,
                allows_multiple_answers=True,
            )
            # Save some info about the poll the bot_data for later use in receive_poll_answer
            payload = {
                message.poll.id: {
                    "questions": event_dates,
                    "message_id": message.message_id,
                    "chat_id": update.effective_chat.id,
                    "answers": 0,
                }
            }

            # TODO poll id should probably be stored on DB
            context.bot_data.update(payload)
            return State.VOTING
        pass
    else:
        update.message.reply_text('This command can only be issued in a group')

def close_poll(update: Update, context: CallbackContext) -> State:
    pass

def query_event(event_id: str):
    return {
        'id' : event_id,
        'name' : 'Test event',
        'dates' : ['05.12.2020', '06.12.2020', '10.12.2020'],
        'organizer' : 'unknown4048'
    }

def kick_out(update: Update, context: CallbackContext) -> None:
    if update.effective_chat.type != 'group':
        return None
    else:
        button = [["I'm in !", "I'm out !"]]
        update.message.reply_text("Will you be in this event ?", reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True))
        if (update.effective_message.text == "I'm out") :
            update.effective_chat.kick_member(user_id=update.effective_message.from_user.id)
            return
        ...

def register(dispatcher: Dispatcher):
    dispatcher.add_handler(ConversationHandler([CommandHandler('groupstart', group_start)], {
        State.VOTING : [CommandHandler('closepoll', close_poll)],
    }, []))
