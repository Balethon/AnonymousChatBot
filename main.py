from balethon import Client, conditions
from balethon.objects import Message

import config

bot = Client(config.TOKEN)


@bot.on_command()
async def start(*, message: Message):
    await message.reply("Hello")


@bot.on_message(conditions.at_state(None))
async def none_state(message: Message):
    await message.reply("give name")
    message.author.set_state("NAME")


@bot.on_message(conditions.at_state("NAME"))
async def name_state(message: Message):
    await message.reply("give age")
    message.author.set_state("AGE")


@bot.on_message(conditions.at_state("AGE"))
async def age_state(message: Message):
    await message.reply("salam")
    message.author.set_state("MAIN")


@bot.on_message(conditions.at_state("MAIN"))
async def main_state(message: Message):
    await message.reply("you are in main")


if __name__ == "__main__":
    bot.run()
