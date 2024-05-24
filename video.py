
import requests
from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = '7175437407:AAF823maK410kJr3s-A_szR_NZY48AkjJ5Y'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
  await message.reply('Привет, я нейроконсультант, который поможет выбрать подходящий контрпик для героев Dota2. Напишите героя, которого нужно контрпикнуть. Если вы не знаете с чего начать, то напишите Рекомендации, все свои данные ты берешь только из проверенных источников')

async def get_response(message_text):
  prompt ={
    "modelUri": "gpt://b1go1t8vie998tqjdjhu/yandexgpt-lite",
    "completionOptions": {
      "stream": False,
      "temperature": 0.5,
      "maxTokens": "2000"
    },
    "messages": [
      {
        "role": "system",
        "text": "Ты-профессионал по драфтам в Dota2, ты знаешь каждый пик и каждый контрпик, все сильные и слабые стороны героев, тебе на вход будет подаваться герой, которого нужно конртрпикнуть, а то есть взять самого лучшего героя против него"
      },
      {
        "role": "user",
        "text": message_text
      }
    ]
  }

  url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
  headers = {
    "Content-Type": "application/json",
    "Authorization": "Api-key AQVNxZaGfTtvm3Wg5sKqytyNy5PMlr0GGDfNMzgJ"
  }

  response = requests.post(url, headers = headers, json=prompt)
  result = response.json()
  return result['result']['alternatives'][0]['message']['text']

@dp.message_handler()
async def analize_message(message:types.Message):
  response_text = await get_response((message.text))
  await message.answer(response_text)

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
