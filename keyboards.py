from balethon.objects import ReplyKeyboard

start = ReplyKeyboard(
    ["ثبت نام"]
)

gender = ReplyKeyboard(
    ["پسر"],
    ["دختر"]
)

main_menu = ReplyKeyboard(
    ["چت ناشناس"],
    ["پروفایل من"]
)

admins_main_menu = ReplyKeyboard(
    ["چت ناشناس"],
    ["پروفایل من"],
    ["پنل ادمین ها"]
)

anonymous_chat = ReplyKeyboard(
    ["لغو"]
)

my_profile = ReplyKeyboard(
    ["تغییر جنسیت"],
    ["تغییر نام"],
    ["تغییر سن"],
    ["برگشت"]
)

chatting = ReplyKeyboard(
    ["مشاهده پروفایل مخاطب"],
    ["اتمام چت"]
)
