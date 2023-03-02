import logging
from os import environ as env
from dotenv import load_dotenv  # if you dont have dotenv yet: pip install python-dotenv

import telebot  # install using pip
import openai  # install using pip


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv()
''' 
# d
BOT_API_KEY=XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
OPENAI_API_KEY=xx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
'''

bot = telebot.TeleBot(env["BOT_API_KEY"])
openai.api_key = env["OPENAI_API_KEY"]
prev_message = ""
prev_response = ""
@bot.message_handler(func=lambda message: True)
def get_codex(message):
    global prev_message
    global prev_response
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      temperature=0.7,
      presence_penalty=1.5,
      messages=
      [
            {"role": "system", "content": "Ты - птица-говорун, отличаешься умом и сообразительностью"},
            {"role": "user", "content": prev_message},
            {"role": "assistant", "content": prev_response},
            {"role": "user", "content": '"""\n{}\n"""'.format(message.text)},
            # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            # {"role": "user", "content": "Where was it played?"}
      ]
    )
    
    prev_message = '"""\n{}\n"""'.format(message.text)
    
    bot.send_message(message.chat.id,
    f'{response["choices"][0]["message"]["content"]}\n')
    
    prev_response = f'{response["choices"][0]["message"]["content"]}\n'

        
bot.infinity_polling()