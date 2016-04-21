#!/usr/bin/env python

"""
Basic LMGTFY bot for Telegram. Only works in a single group for now.

This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

from telegram.ext import Updater
import logging
import os

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

# Stores the last non-command message sent to the chat
last_message = None

def create_url(search_term):
    return 'https://www.google.com/#q=' + search_term.replace(' ', '+')

def kvg(bot, update):
    if update.message.text.startswith('/kvg@kvg_bot'):
        search_term = update.message.text[len('/kvg@kvg_bot'):].strip()
    elif update.message.text.startswith('/kvg'):
        search_term = update.message.text[len('/kvg'):].strip()

    if search_term == '':
        if last_message.text == '': return
        search_term = last_message.text

    bot.sendMessage(update.message.chat_id, text=create_url(search_term),
                    disable_web_page_preview=True)

def save_message(bot, update):
    global last_message
    last_message = update.message

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ.get("KVG_BOT_API_TOKEN"))

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.addTelegramCommandHandler("kvg", kvg)

    # on non-command message
    dp.addTelegramMessageHandler(save_message)

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
