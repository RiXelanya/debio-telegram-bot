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

ROLE, SELECTANALYSIS, ADDANALYSIS, OPTIONANALYSIS, OPTIONANALYST, SELECTTEST, ADDTEST, OPTIONTEST = range(8)
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

def analysis(update: Update, context: CallbackContext) -> int :
    username = update.message.from_user.username
    update.message.reply_text("Hi, Do you want to upload genetic data or not?")

    return OPTIONANALYSIS

def option_analysis(update: Update, context: CallbackContext) -> int :
    username = update.message.from_user.username
    update.message.reply_text("Hi, Do you want to upload genetic data or not?")
    content = update.message.text

    if (content == 'yes') :
        return ADDANALYSIS
    elif (content == 'no') :
        return SELECTANALYSIS
    else :
        update.message.reply_text('Input unknown.')
        return ConversationHandler.END
    
def add_analysis(update: Update, context: CallbackContext) -> int :
    update.message.reply_text("Please upload your genetic data")
    return ConversationHandler.END

def option_analyst(update: Update, context: CallbackContext) -> int :
    update.message.reply_text("Please select genetic analyst")
    return ConversationHandler.END

def select_analysis(update: Update, context: CallbackContext) -> int :
    update.message.reply_text("Please Select Genetic Data To be Sent to Genetic Analyst")
    return ConversationHandler.END

def option_test(update: Update, context: CallbackContext) -> int :
    update.message.reply_text("Please Select the test provider")
    return ConversationHandler.END

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

    analysis_handler = ConversationHandler(
        entry_points=[CommandHandler('analysis', analysis)],
        states={
            OPTIONANALYSIS: [MessageHandler(Filters.text & ~Filters.command, option_analysis)],
            OPTIONANALYST: [MessageHandler(Filters.text & ~Filters.command, option_analyst)],
            SELECTANALYSIS: [MessageHandler(Filters.text & ~Filters.command, select_analysis)],
            ADDANALYSIS: [MessageHandler(Filters.text & ~Filters.command, add_analysis)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(analysis_handler)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('orders', order))
    dispatcher.add_handler(CommandHandler('tests', option_test))
    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == "__main__":
    main()