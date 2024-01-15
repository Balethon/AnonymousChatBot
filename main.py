from balethon import Client
from balethon.objects import Message

import config

bot = Client(config.TOKEN)


@bot.on_message()
async def answer_message(message: Message):
    await message.reply(message.text)


if __name__ == "__main__":
    bot.run()
