import telebot
from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import numpy as np
from flask import Flask, request
import os

bot_token = '897203128:AAG62vz8NGvXRbjOZnmigwzh_jVouM2P9LE'
bot = telebot.TeleBot(token=bot_token)
server = Flask(__name__)
@bot.message_handler(commands=['start'])  # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'welcome')
@bot.message_handler(commands=['help'])  # help message handler
def send_welcome(message):
    bot.reply_to(message, 'ALPHA = FEATURES MAY NOT WORK')


@bot.message_handler(func=lambda msg: msg.text is not None and '@' in msg.text)
# lambda function finds messages with the '@' sign in them
# in case msg.text doesn't exist, the handler doesn't process it
def at_converter(message):
    texts = message.text.split()
    at_text = findat(texts)
    if at_text == '@':  # in case it's just the '@', skip
        pass
    else:
        insta_link = "https://instagram.com/{}".format(at_text[1:])
        bot.reply_to(message, insta_link)



@bot.message_handler(commands=['help'])  # help message handler
def send_welcome(message):
    bot.reply_to(message, 'ALPHA = FEATURES MAY NOT WORK')

URL = requests.get('https://www.sharesansar.com/datewise-indices')
souped = BS(URL.content, 'html.parser')
table = souped.find('tbody') #works good till here
# ######################
nepse_trfinder = table.find('tr')
#print(nepse_trfinder)
nepse_trfinder1 = nepse_trfinder.find_all('td')
single_row_data =[td.text.strip() for td in nepse_trfinder1]
# print(single_row_data)
final_data= pd.DataFrame([single_row_data],columns=['Index','Point','Number change','percentage'])

# @bot.message_handler(func= lambda msg: msg is not None)
# def send_welcome(message):
#     bot.reply_to(message,'Thank you for using this program')
#
@bot.message_handler(commands=['nepse'])  # help message handler
def send_welcome(message):
    bot.reply_to(message, final_data)

@server.route('/' + bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://pure-sands-38023.herokuapp.com/' + bot_token)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))