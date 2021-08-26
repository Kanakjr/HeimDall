################################
#  Code Author: Kanak Dahake   #
################################

import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
import requests

update_id = None

def main():
    global update_id
    bot = telegram.Bot('1115657037:AAG4__sJ9JWa1zh-dLmbC6F4bifhh2o5iEI') # HeimDall Telegram Bot AccessID
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            reply(bot)
        except NetworkError:
            sleep(0.1)
        except Unauthorized:
            update_id += 1

def httpresponse(inputt):
    try:
        response = requests.get('http://127.0.0.1:5000/response?userid=123&input='+inputt).json()
        return response["response"]
    except requests.exceptions.RequestException as e:  
        return "HeimDall Server Connection Error" #str(e)
        
def echo(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:  
            update.message.reply_text(update.message.text)
            
def reply(bot):
    global update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        if update.message:  
            update.message.reply_text(httpresponse(update.message.text))

if __name__ == '__main__':
    main()