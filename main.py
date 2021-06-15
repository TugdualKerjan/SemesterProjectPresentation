from io import BytesIO

import cv2
import numpy as np
import telegram
from dotenv import dotenv_values
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import NetworkError, Unauthorized
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from logoclassify import classify
from logodetect import predict

config = dotenv_values(".env")
token = config['SECRET_KEY']
updater = Updater(token=token, use_context=True)

def main():
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.photo, receive_images))

    updater.start_polling()

def receive_images(update, context):
    user_id = int(update.message.from_user['id'])
    username = update.message.from_user['username']

    decode_img = cv2.imdecode(np.frombuffer(BytesIO(context.bot.getFile(update.message.photo[-1].file_id).download_as_bytearray()).getbuffer(), np.uint8), -1)
    context.bot.sendMessage(update.effective_chat.id, "Preparing glasses and brains...")

    stickers = predict(decode_img)
    for subimage in stickers:
        buffer = cv2.imencode(".png", subimage)[1].tobytes()
        logo = classify(subimage)
        context.bot.sendMessage(update.effective_chat.id, "Class it belongs to : %s" % str(logo))
        context.bot.sendPhoto(update.effective_chat.id, buffer)
    
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="""Hey! Send me a message with a picture and I'll cut it out for you!""")


if __name__ == '__main__':
    main()
