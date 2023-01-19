from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes
from aiogram.utils import executor
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yookassa import Configuration, Payment
from datetime import datetime


import json_file
import keyboards
import settings
import additional_foos
import texts
import keyboards




#create Aiogram dispatcher
import texts

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot)

dict_users = dict()


#setup YOUKASSA
Configuration.account_id = settings.YOUKASSA_account_id
Configuration.secret_key = settings.YOUKASSA_secret_key

admin_list = [658697862, 492213965]


@dp.message_handler()
async def main_messages(message: types.Message):
    global dict_users
    print(message)
    if message.text[0:4].lower() == "7171":
        for el in dict_users.keys():
            await  bot.send_message(str(el), message.text[4:])
    if "get_video" in message.text:
       # try:
            num = message.text[9]
            print(additional_foos.get_video_id([num]))
            if num == -1:
                await  bot.send_message(message.chat.id, f"Can't find video {num}")
            else:
                try:
                    await bot.send_video(message.chat.id, additional_foos.get_video_id(num))
                except Exeption as Ex:
                    print("Error Send Admin Video")
                    print(Ex)

    if additional_foos.checking_new_user(dict_users, message.chat.id) == 1: # If user doesn't exist
        dict_users = additional_foos.reg_new_user(dict_users, message)
        # Send greeting_text
        # Send try_keyboard
        greeting_text = texts.greetting_text
        await bot.send_message(message.chat.id, greeting_text,  reply_markup = keyboards.try_class_keyboard)
    else: # User exist
        # Проверяем последнее взаимодействие пользователя с ботом.
        if await additional_foos.last_msg_time_more(dict_users[str(message.chat.id)][3]):
            await bot.send_message(message.chat.id, texts.text_two_weeks)

        await update_time(message.chat.id)

        command = message.text
        if command == "/start_class":
            if dict_users[str(message.chat.id)][1] > 0:
                asyncio.create_task(send_class(message.chat.id, settings.time_delete_active_lesson,
                                               message.message_id))
            else:
                await bot.send_message(message.chat.id, texts.text_zero_classes)
        elif command == "/show_left":
            text = texts.left_classes(message.chat.id, dict_users)
            await bot.send_message(message.chat.id, text)
        elif command == "/follow":
            await follow_command(message.chat.id)
        #elif command == "/add_video":
        #    print(message)


####КОПИЯ СТАРТ###
@dp.message_handler(content_types = types.ContentType.ANY)
async def start(message: types.Message):
    if message.chat.id in admin_list:
        print(type(message.video.file_id))

        additional_foos.add_video_to_db(message.video.file_id)
        #print(message)

async def update_time(chat_id:int):
    global dict_users
    timestamp = int(datetime.today().timestamp())
    dict_users[str(chat_id)][3] = timestamp
    json_file.save_json(dict_users)


async def follow_command(chat_id):
    global dict_users
    if dict_users[str(chat_id)][1] > 0:
        await bot.send_message(chat_id,
                               f"Доступных занятий осталось: {dict_users[str(chat_id)][1]}\n")
    else:
        sale = False
        if "sale" in dict_users[str(chat_id)]:
            sale = True
        else:
            print(len(dict_users[str(chat_id)]))

        if sale:
            await bot.send_photo(chat_id, photo=settings.sale_picture_link,
                                 reply_markup=keyboards.classes_keyboard)
        else:
            await bot.send_message(chat_id, texts.follow_text(sale), reply_markup=keyboards.classes_keyboard)

@dp.callback_query_handler()
async def callback(call: types.CallbackQuery):
    global dict_users
    if call.data == "try":
        # Удаляем кнопку
        await bot.delete_message(call.message.chat.id,
                                 message_id=call.message.message_id)
        # Отправляем пробное занятие
        asyncio.create_task(send_class(call.message.chat.id,
                                       settings.time_delete_try_lesson,
                                       call.message.message_id))
        await asyncio.sleep(5)
        # Отправляем сообщение
        await bot.send_message(call.message.chat.id,
                               texts.text_after_try_class)
        await asyncio.sleep(5)
        # Предлагаем скидку
        await bot.send_message(call.message.chat.id,
                               "Скидка на приобритение занятия действует три часа",
                               reply_markup=keyboards.sale_class_keyboard)

    elif "cl_" in call.data:
        await bot.delete_message(call.message.chat.id,
                                 message_id=call.message.message_id)
        text = texts.agreement_text
        await bot.send_message(call.message.chat.id, text)

        if call.data == "cl_5":
            summ_for_payment = settings.summ_5_cl
            q_cl = 5
        elif call.data == "cl_10":
            summ_for_payment = settings.summ_10_cl
            q_cl = 10
        elif call.data == "cl_30":
            summ_for_payment = settings.summ_30_cl
            q_cl = 30
        if "sale" in dict_users[str(call.message.chat.id)]:
            summ_for_payment *= 0.8;
        print(f"summ: {summ_for_payment}")
        await payments(summ_for_payment, q_cl, call.message.chat.id)


    elif call.data == "sale":
        await bot.delete_message(call.message.chat.id,
                                 message_id=call.message.message_id)
        asyncio.create_task(get_sale(call.message.chat.id,
                                       settings.time_delete_try_lesson,
                                       call.message.message_id))
        await asyncio.sleep(3)
        await follow_command(call.message.chat.id)


async def get_sale(chat_id:int, time:int, msg_id):
    # добавляем к базе данных скидочный пункт, через три часа удаляем
    global dict_users
    dict_users[str(chat_id)].append("sale")
    json_file.save_json(dict_users)

    await asyncio.sleep(settings.time_sale)
    while True:
        try:
            dict_users[str(chat_id)].remove("sale")
        except:
            break
    json_file.save_json(dict_users)

async def payments(summ_for_payment:int, q_cl:int, chat_id:int):
    # ЗАТЫЧКА!!!!
    # summ_for_payment = 100

    description = f"Предоплата за {q_cl} занятий Йога Пробуждения."

    ####
    payment = Payment.create({
        "amount": {
            "value": f"{summ_for_payment}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/yoga_time_awakening_bot"
        },
        "capture": True,
        "description": f"{description}",
        "metadata": {
            "order_id": "0"
        }})

    ###ЗАТЫЧКА!!!
    payment_url = payment.confirmation.confirmation_url
    #payment_url = "vk.com"

    inline_button_url = InlineKeyboardButton('Перейти на страницу оплаты.', url=payment_url)
    inline_keyboard_url = InlineKeyboardMarkup().add(inline_button_url)

    text = ('Остался последний шаг!\n'
            'Переходите на страницу оплаты, чтобы пройти новый путь!\n')


    photo_url = "https://yapx.ru/v/UVD8w"
    await bot.send_photo(chat_id, photo=photo_url, caption=text, reply_markup=inline_keyboard_url)
    task = asyncio.create_task(check_pay(chat_id, payment.id, q_cl))

async def send_confirm_message_adm(chat_id:int, q_classes:int):
    text = (f"Пользователь приобрел {q_classes} занятий.\n"
            f"Id пользователя: {chat_id}\n"
            f"Имя пользователя: {dict_users[str(chat_id)][0]}\n" )
    for admin_id in admin_list:
        await bot.send_message(admin_id, text)

async def check_pay(chat_id, payment_id, q_classes):
    global dict_of_users
    confirm = False
    wait = 0
    while confirm == False:
        # Запрашиваем статус платежа
        payment = Payment.find_one(payment_id)
        status = payment.status
        # ЗАТЫЧКА!
        await asyncio.sleep(5)
        status = "succeeded"
        ##############
        if status == "succeeded":
            await bot.send_message(chat_id, "Платеж проведен успешно.")
            await got_payment(chat_id, q_classes)
            await send_confirm_message_adm(chat_id, q_classes)
            return 0
        elif status == "canceled":
            await bot.send_message(chat_id, "Ошибка платежа. Повторите попытку.")
            confirm = True
            return 1
        await asyncio.sleep(5)
        wait = wait + 5
        if wait > 600:
            await bot.send_message(chat_id, "Время платежа истекло.")
            confirm = True


async def got_payment(chat_id:int, q_classes:int):
    global dict_users
    dict_users[str(chat_id)][1] += q_classes
    json_file.save_json(dict_users)
    await bot.send_message(chat_id, texts.left_classes(chat_id, dict_users))

async def send_class(chat_id:int, time:int, msg_id):
    global dict_users
    if dict_users[str(chat_id)][1] == 0:
        f_id = additional_foos.get_video_id(0)
        await bot.send_video(chat_id, f_id, protect_content=True)
        await asyncio.sleep(time)
    elif dict_users[str(chat_id)][1] > 0:
        f_id = additional_foos.get_video_id(dict_users[str(chat_id)][2])
        await bot.send_video(chat_id, f_id, protect_content=True)
        dict_users = additional_foos.MinusDay_PlusNumClass_UpdateJson(chat_id, dict_users)
        await asyncio.sleep(time)
    try:
        await bot.delete_message(chat_id, msg_id+1)
    except:
        print("Error delete_message in foo send_class\n")

async def start_async(x):
    print(x)
    asyncio.create_task(check_t())

async def check_t():
    print("254")
    global dict_users
    while True:
        for key, value in dict_users.items():
            if await additional_foos.last_msg_time_more(dict_users[str(key)][3]):
                print("259")
                await bot.send_message(int(key), texts.text_no_two_weeks)
                await update_time(int(key))

        await asyncio.sleep(5)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # При запуске всегда делать инициализацию словаря.
    dict_users = json_file.init_json()
    if (dict_users == 1):
        print("Error init json\n")
        print("Dict_users Empty\n")
        dict_users = dict()
    else:
        print("Success init json\n")
    executor.start_polling(dp, skip_updates=True, on_startup=start_async)
    try:
        pass
        #executor.start_polling(dp, skip_updates=True, on_startup=start_async)
    except Exception as Ex:
        print("Error start polling: Ex: " + Ex)
