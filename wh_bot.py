from flask import Flask, request, jsonify
import requests 
import json

app = Flask(__name__)

URL = 'https://api.telegram.org/bot1218173285:AAHDGQPjL3g610h-AxPcwldCuYSFUD3pvQc/'

def send_message(chat_id, text='bla-bla-bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id' : chat_id, 'text' : text}
    r = requests.post(url, json = answer)
    return r.json() 


# https://api.telegram.Sorg/bot1281146714:AAEQT6wJlPN6xPYoGqLQeeZmaCSO3hJx0vQ/setWebhook?url=https://3e2fd298.ngrok.io/
# 
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']
        print(chat_id, message)
        send_message(chat_id, message)
    print('yo')
    return '<h1>Hello!</h1>'

if __name__ == '__main__':
    app.run(
        host='213.139.208.120',
	port=88
        #ssl_context= (
        #    '/etc/letsencrypt/live/pugovkabot.ru/cert.pem', 
        #    '/etc/letsencrypt/live/pugovkabot.ru/privkey.pem'
        #)
    )
    


# if __name__ == "__main__":
#         main()
# def write_json(data,file_name='answer.json'):
#     with open(file_name,'w') as f:
#         json.dump(data,f,indent=2,ensure_ascii=False)#indent - отступы, 


# def get_updates():#getting updates from telegram server
#     URL = url + 'getUpdates'
#     r = requests.get(URL)
#     write_json(r.json(),'updates.json')
#     return r.json()



#  try:
#             update_id = echo(bot, update_id)
#         except telegram.TelegramError as e:
#             # These are network problems with Telegram.
#             if e.message in ("Bad Gateway", "Timed out"):
#                 sleep(1)
#             elif e.message == "Unauthorized":
#                 # The user has removed or blocked the bot.
#                 update_id += 1
#             else:
#                 raise e
#         except URLError as e:
            # These are network problems on our end.