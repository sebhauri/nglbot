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

class State(Enum):
    SLEEP = 0
    START = 1
    DATE = 2

TOKEN = '1432985981:AAHxLzTlnqVH8uo20PPuhDFSqbWqp6hBlJw'

def start(update: Update, context: CallbackContext) -> None:
    context.user_data['state'] = State.START

    button = [["Yes !", "No :("]]
    update.effective_message.reply_text(
        "Welcome ! Would you like to creat an event ?", reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=True)
    )

def resp(update: Update, context: CallbackContext):
    switcher = {
        State.SLEEP : sleep_response,
        State.START : start_response,
        State.DATE : date_response,
    }

    state = context.user_data['state']
    switcher.get(state, error_response)(update, context)
    

def error_response(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Something went wrong, please start over with /start")

def sleep_response(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Use /start to start planning an event")

def start_response(update: Update, context: CallbackContext) -> None:
    if 'No :(' == update.effective_message.text:
        context.user_data['state'] = State.SLEEP
        update.message.reply_text("Sorry to see you go :(")
    elif 'Yes !' == update.effective_message.text:
        context.user_data['state'] = State.DATE
        update.message.reply_text("Propose a date (format : dd/mm)")

def date_response(update: Update, context: CallbackContext) -> None:
    context.user_data['state'] = State.SLEEP
    update.message.reply_text(f"Your date is : {update.effective_message.text}")


def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    #Commands handlers
    dispatcher.add_handler(ConversationHandler(CommandHandler('start', start), {State.SLEEP:}))
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    #Commands handlers
    dispatcher.add_handler(CommandHandler('start', start))
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    #Commands handlers
    dispatcher.add_handler(CommandHandler('start', start))
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    #Commands handlers
    dispatcher.add_handler(CommandHandler('start', start))
    
    #Message handlers
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), resp))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()