from balethon import Client, conditions
from balethon.objects import Message

import config
import texts
import keyboards
from database import Database

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
    user = Database.load_user(message.author.id)
    user.name = message.text

    await message.reply(texts.give_age)
    message.author.set_state("AGE")


@bot.on_message(conditions.at_state("AGE"))
async def age_state(message: Message):
    user = Database.load_user(message.author.id)
    user.age = message.text

    await message.reply(texts.main_menu, keyboards.main_menu)
    message.author.set_state("MAIN")


@bot.on_message(conditions.at_state("MAIN") & conditions.regex(f"^چت ناشناس$"))
async def anonymous_chat(message: Message):
    await message.reply(texts.anonymous_chat, keyboards.anonymous_chat)
    message.author.set_state("SEARCHING")


@bot.on_message(conditions.at_state("SEARCHING") & conditions.regex(f"^لغو$"))
async def cancel(message: Message):
    await message.reply(texts.cancel, keyboards.main_menu)


@bot.on_message(conditions.at_state("MAIN") & conditions.regex(f"^پروفایل من$"))
async def my_profile(message: Message):
    user = Database.load_user(message.author.id)

    await message.reply(f"{texts.my_profile}: {user}", keyboards.my_profile)


if __name__ == "__main__":
    bot.run()
