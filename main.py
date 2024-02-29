import json
import requests
import os
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, ConversationHandler
from telegram.ext import filters  # This is the updated import statement
callback_url = "https://app.myriad.social/login"
from datetime import datetime
from bs4 import BeautifulSoup

ROLE = range(1)
walletAddress = '5HmprRDh4yqrHuinU8C9HwQzdvvZ7UP8UBY1jBC6KrPNReee'
baseurl = 'https://api.testnet.debio.network'

def start(update: Update, context: CallbackContext) -> int:
    username = update.message.from_user.username
    chat_type = update.message.chat.type

    if not username:
        update.message.reply_text('Sorry, the Debio bot requires you to have set a Telegram @username. Please go to your Telegram settings to set a @username of your own. After you have done so, you may press /start again.')
        return
    
    update.message.reply_text("Hi, please select your role")
    return ROLE

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def role(update: Update, context: CallbackContext) -> int :
    return ConversationHandler.END

def order(update: Update, context: CallbackContext) -> int :
    url = f"{baseurl}/order/list/{walletAddress}"
    response = requests.get(url)
    if response.status_code == 200 :
        update.message.reply_text(response)
    else :
        update.message.reply_text("Cant get Orders List")


    return ConversationHandler.END

def notification(update: Update, context: CallbackContext) -> int :
    url = f"{baseurl}/notification/{walletAddress}"
    response = requests.get(url)
    if response.status_code == 200 :
        update.message.reply_text(response)
    else :
        update.message.reply_text("Cant get Notification List")


    return ConversationHandler.END


def main():

    # Replace YOUR_API_KEY with your actual Telegram API key (not the Myriad api key)
    updater = Updater(":")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ROLE: [MessageHandler(Filters.text & ~Filters.command, role)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('orders', order))
    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == "__main__":
    main()