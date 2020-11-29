from telegram.ext import (
    Updater,
    MessageHandler,
    ConversationHandler,
    Filters,
    CallbackContext,
    Dispatcher
)

from telegram import (
    Update,
)


def echo(update, context):
    if 'vrai' in update.message.text:
        update.effective_message.reply_text("Ouais, c'est pas faux !", reply_to_message_id=update.effective_message.message_id)

def register(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))



