from balethon import Client, conditions
from balethon.objects import Message, KeyboardRemove, User
from balethon.states import StateMachine

import config
import texts
import keyboards
from database import Database

bot = Client(config.TOKEN)

User.state_machine = StateMachine("user_states.db")


def is_intable(string):
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True


@bot.on_message(chain="print")
def print_message(message: Message):
    print(f"{message.author.full_name}: {message.text or message.caption or ''}")


@bot.on_command()
async def start(*, message: Message):
    user = Database.load_user(message.author.id)

    if user.needs_registration():
        await message.reply(texts.start, keyboards.start)

    else:
        await message.reply(texts.start, keyboards.main_menu)
        message.author.set_state("MAIN")


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
    if not is_intable(message.text):
        return await message.reply(texts.invalid_age)

    age = int(message.text)

    if age < 10:
        return await message.reply(texts.age_too_low)

    if age > 99:
        return await message.reply(texts.age_too_high)

    user = Database.load_user(message.author.id)
    user.age = age
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
        match.match_id = message.author.id
        Database.save_user(match)
        await client.send_message(match.id, texts.found_match, keyboards.chatting)
        User.state_machine[match.id] = "CHATTING"

        user = Database.load_user(message.author.id)
        user.match_id = match.id
        Database.save_user(user)
        await message.reply(texts.found_match, keyboards.chatting)
        message.author.set_state("CHATTING")

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


@bot.on_message(conditions.at_state("CHATTING") & conditions.regex(f"^مشاهده پروفایل مخاطب$"))
async def see_profile(message: Message):
    user = Database.load_user(message.author.id)
    match = user.get_match()

    await message.reply(f"{texts.match_profile}\n{match}")


@bot.on_message(conditions.at_state("CHATTING") & conditions.regex(f"^اتمام چت$"))
async def back(client: Client, message: Message):
    await message.reply(texts.you_ended_chat, keyboards.main_menu)
    message.author.set_state("MAIN")

    user = Database.load_user(message.author.id)
    match = user.get_match()

    await client.send_message(match.id, texts.match_ended_chat, keyboards.main_menu)
    User.state_machine[match.id] = "MAIN"


@bot.on_message(conditions.at_state("CHATTING"))
async def chatting(message: Message):
    user = Database.load_user(message.author.id)

    await message.copy(user.match_id)


if __name__ == "__main__":
    bot.run()
