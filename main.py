from balethon import Client, conditions
from balethon.objects import Message

import config
import texts
import keyboards

bot = Client(config.TOKEN)


@bot.on_command()
async def start(*, message: Message):
    await message.reply(texts.start, keyboards.start)


@bot.on_message(conditions.at_state(None))
async def none_state(message: Message):
    await message.reply(texts.give_name)
    message.author.set_state("NAME")


@bot.on_message(conditions.at_state("NAME"))
async def name_state(message: Message):
    await message.reply(texts.give_age)
    message.author.set_state("AGE")


@bot.on_message(conditions.at_state("AGE"))
async def age_state(message: Message):
    await message.reply(texts.main_menu, keyboards.main_menu)
    message.author.set_state("MAIN")


@bot.on_message(conditions.at_state("MAIN"))
async def main_state(message: Message):
    await message.reply(texts.main_menu, keyboards.main_menu)


if __name__ == "__main__":
    bot.run()
