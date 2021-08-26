import telegram

bot = telegram.Bot('1115657037:AAG4__sJ9JWa1zh-dLmbC6F4bifhh2o5iEI')
chatID = '890867052' #Change based on group or user

def sendText(text):
    bot.send_message(chat_id=chatID,text=text)
    
def sendPhoto(url,local=False):
    if local:
        url = open(url,'rb')
    bot.sendPhoto(chat_id=chatID,photo=url)
    
def sendDoc(url,local=False):
    if local:
        url = open(url,'rb')
    bot.sendDocument(chat_id=chatID,document=url)