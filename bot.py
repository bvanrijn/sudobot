# -*- coding: utf-8 -*-

import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import subprocess
import time
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


config = configparser.ConfigParser()
config.read('bot.ini')

updater = Updater(token=config['KEYS']['bot_api'])
dispatcher = updater.dispatcher


def start(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=ChatAction.TYPING)
    bot.sendMessage(chat_id=update.message.chat_id, text="Hi. I'm sudobot.")
    if update.message.from_user.id != int(config['ADMIN']['id']):
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        time.sleep(1)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="It seems like you aren't allowed to use me. :(")
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        time.sleep(1.5)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="But sudobot is open source software, which means you can have your own! See my [GitHub repo](https://github.com/bvanrijn/sudobot) for details.", parse_mode="Markdown")
    else:
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        time.sleep(1)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="You can use me to run commands on your computer or server.")
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        time.sleep(1.5)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Note that interactive commands or commands that generate a lot of output won't work.")
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        time.sleep(1)
        bot.sendMessage(chat_id=update.message.chat_id, text="Have fun!")
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        time.sleep(1.5)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Oh, before I forget: sudobot is open source software. See my [GitHub repo](https://github.com/bvanrijn/sudobot).", parse_mode="Markdown")


def execute(bot, update):
    if update.message.from_user.id == int(config['ADMIN']['id']):
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=ChatAction.TYPING)
        output = subprocess.Popen(
            update.message.text, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = output.stdout.read().decode('utf-8')
        output = '`{0}`'.format(output)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=output, parse_mode="Markdown")


start_handler = CommandHandler('start', start)
execute_handler = MessageHandler([Filters.text], execute)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(execute_handler)

dispatcher.add_error_handler(error)

updater.start_polling()
updater.idle()
