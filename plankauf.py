from datetime import datetime
import time
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import telebot
from telebot import types

bot = telebot.TeleBot('<TelegramBotToken>') #  Input your Bot token from paragraph 3

CREDENTIALS_FILE = '<Credential JsonFile of your gserviceaccount>' #  Input the name of your credentials file from paragraph 1 or the path to it
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
['https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

spreadsheetId = '<id of your Google Sheet>' #  Input your spreadsheet ID from paragraph 2
range_name = 'ListTitle!A:F' #  Input name of your list, !, and the range of cells from pargraph 2
table = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range_name).execute()

Employee_dict = {'Smith': 3, 'Muller': 5, 'Meier': 7, 'Wilson': 9, 'Schneider': 11}
Employee_reason_dict = {'Smith': 4, 'Muller': 6, 'Meier': 8, 'Wilson': 10, 'Schneider': 12}
Item_dict = {'Pen': 'B', 'Paper': 'C','Wasser': 'D','Coffee': 'E','Other': 'F'}

name = ''
item = ''
reason = ''

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/order':
        bot.register_next_step_handler(message, get_name)
        markup = telebot.types.ReplyKeyboardMarkup(True)
        markup.add(telebot.types.InlineKeyboardButton(text='Smith', callback_data='Smith'))
        markup.add(telebot.types.InlineKeyboardButton(text='Muller', callback_data='Muller'))
        markup.add(telebot.types.InlineKeyboardButton(text='Meier', callback_data='Meier'))
        markup.add(telebot.types.InlineKeyboardButton(text='Wilson', callback_data='Wilson'))
        markup.add(telebot.types.InlineKeyboardButton(text='Schneider', callback_data='Schneider'))
        bot.send_message(message.chat.id, text="Choose your lastname", reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Write /order')

def get_name(message):
    global name
    name = message.text
    markup = telebot.types.ReplyKeyboardMarkup(True)
    markup.add(telebot.types.InlineKeyboardButton(text='Pen', callback_data='Pen'))
    markup.add(telebot.types.InlineKeyboardButton(text='Paper', callback_data='Paper'))
    markup.add(telebot.types.InlineKeyboardButton(text='Water', callback_data='Water'))
    markup.add(telebot.types.InlineKeyboardButton(text='Coffee', callback_data='Coffee'))
    markup.add(telebot.types.InlineKeyboardButton(text='Other', callback_data='Other'))
    bot.send_message(message.chat.id, text='What you want to order', reply_markup=markup)
    bot.register_next_step_handler(message, get_item)

def get_item(message):
    global item
    item = message.text
    markup = telebot.types.ReplyKeyboardMarkup(True)
    markup.add(telebot.types.InlineKeyboardButton(text='Ended up', callback_data='Ended up'))
    markup.add(telebot.types.InlineKeyboardButton(text='Ends', callback_data='Ends'))
    bot.send_message(message.chat.id, 'You can choose a reason or indicate your own', reply_markup=markup)
    bot.register_next_step_handler(message, get_reason)

def get_reason(message):
    global reason
    reason = message.text
    markup = telebot.types.ReplyKeyboardMarkup(True)
    markup.add(telebot.types.InlineKeyboardButton(text='1', callback_data='1'))
    markup.add(telebot.types.InlineKeyboardButton(text='2', callback_data='2'))
    markup.add(telebot.types.InlineKeyboardButton(text='3', callback_data='3'))
    markup.add(telebot.types.InlineKeyboardButton(text='4', callback_data='4'))
    markup.add(telebot.types.InlineKeyboardButton(text='5', callback_data='5'))
    markup.add(telebot.types.InlineKeyboardButton(text='6', callback_data='6'))
    markup.add(telebot.types.InlineKeyboardButton(text='7', callback_data='7'))
    markup.add(telebot.types.InlineKeyboardButton(text='8', callback_data='8'))
    markup.add(telebot.types.InlineKeyboardButton(text='9', callback_data='9'))
    markup.add(telebot.types.InlineKeyboardButton(text='10', callback_data='10'))
    markup.add(telebot.types.InlineKeyboardButton(text='100', callback_data='100'))
    bot.send_message(message.chat.id, 'How much you want to order?Choose or write the quantity', reply_markup=markup)
    bot.register_next_step_handler(message, get_quantity)

def get_quantity(message):
    try:
        global quantity
        quantity = message.text
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='No', callback_data='no')
        keyboard.add(key_no)
        question = 'Do you want to order ' + str(quantity) + ' ' + item + ', because ' + reason + ", Mr/Mrs" + name + '?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            try:
                if call.data == "yes":
                    #  In the value of the range, you need to put the name of our sheet
                    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, 
                    body={ "valueInputOption": "USER_ENTERED", "data": [{"range": "Listtitle" + "!" +
                    Item_dict.get(item) + str(Employee_dict.get(name)), "majorDimension": "ROWS",
                    "values": [[quantity]]}]}).execute()
                    #  In the value of the range, you need to put the name of our sheet
                    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId,
                    body={"valueInputOption": "USER_ENTERED", "data": [{"range": "Listtitle" + "!" +
                    Item_dict.get(item) + str(Employee_reason_dict.get(name)), "majorDimension": "ROWS",
                    "values": [[reason + ' ' + str(datetime.now().date())]]}]}).execute()
                    bot.send_message(call.message.chat.id, 'Order completed')
                    start(message)
                elif call.data == "no":
                    start(message)
            except Exception:
                bot.send_message(message.from_user.id, 'Choose values from the drop-down lists, '
                                                       'except for order reason and quantity')
                start(message)

    except Exception:
        bot.send_message(message.from_user.id, 'In numbers, please')
        start(message)
try:
    bot.polling(none_stop=True, interval=0)
except Exception:
    time.sleep(100)
    bot.polling(none_stop=True, interval=0)
