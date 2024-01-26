from balethon import Client, conditions
from balethon.objects import Message, KeyboardRemove, User
from balethon.states import StateMachine

import config
import texts
import keyboards
from database import Database

bot = Client(config.TOKEN)

User.state_machine = StateMachine("user_states")


@bot.on_message(chain="print")
def print_message(message: Message):
    print(f"{message.author.full_name}: {message.text}")


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
    Database.save_user(user)

    if user.age is None:
        await message.reply(texts.give_age)
        message.author.set_state("AGE")
    else:
        await message.reply(texts.main_menu, keyboards.main_menu)
        message.author.set_state("MAIN")


@bot.on_message(conditions.at_state("AGE"))
async def age_state(message: Message):
    user = Database.load_user(message.author.id)
    user.age = message.text
    Database.save_user(user)

    await message.reply(texts.main_menu, keyboards.main_menu)
    message.author.set_state("MAIN")


@bot.on_message(conditions.at_state("MAIN") & conditions.regex(f"^چت ناشناس$"))
async def anonymous_chat(client: Client, message: Message):
    cursor = User.state_machine.connection.cursor()
    cursor.execute("SELECT user_id FROM user_states WHERE user_state = ?", ("SEARCHING",))
    user_id = cursor.fetchone()

    if user_id is not None:
        match = Database.load_user(user_id[0])
        await message.reply(texts.found_match)
        message.author.set_state("CHATTING")

        await client.send_message(match.id, texts.found_match)
        User.state_machine[match.id] = "CHATTING"

    else:
        await message.reply(texts.anonymous_chat, keyboards.anonymous_chat)
        message.author.set_state("SEARCHING")


@bot.on_message(conditions.at_state("SEARCHING") & conditions.regex(f"^لغو$"))
async def cancel(message: Message):
    await message.reply(texts.cancel, keyboards.main_menu)
    message.author.set_state("MAIN")


@bot.on_message(conditions.at_state("MAIN") & conditions.regex(f"^پروفایل من$"))
async def my_profile(message: Message):
    user = Database.load_user(message.author.id)

    await message.reply(f"{texts.my_profile}\n{user}", keyboards.my_profile)
    message.author.set_state("PROFILE")


@bot.on_message(conditions.at_state("PROFILE") & conditions.regex(f"^تغییر نام$"))
async def edit_name(message: Message):
    await message.reply(texts.give_name, KeyboardRemove())
    message.author.set_state("NAME")


@bot.on_message(conditions.at_state("PROFILE") & conditions.regex(f"^تغییر سن$"))
async def edit_age(message: Message):
    await message.reply(texts.give_age, KeyboardRemove())
    message.author.set_state("AGE")


@bot.on_message(conditions.at_state("PROFILE") & conditions.regex(f"^برگشت$"))
async def back(message: Message):
    await message.reply(texts.main_menu, keyboards.main_menu)
    message.author.set_state("MAIN")


if __name__ == "__main__":
    bot.run()
