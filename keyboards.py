
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

try_button = InlineKeyboardButton("Пробное занятие", callback_data = "try")
try_class_keyboard= InlineKeyboardMarkup().add(try_button)

sale_button = InlineKeyboardButton("Получить скидку", callback_data = "sale")
sale_class_keyboard = InlineKeyboardMarkup().add(sale_button)


cl5 = InlineKeyboardButton('5 занятий', callback_data = "cl_5")
cl10=InlineKeyboardButton('10 занятий', callback_data = "cl_10")
cl30=InlineKeyboardButton('30 занятий', callback_data = "cl_30")
classes_keyboard= InlineKeyboardMarkup().add(cl5, cl10, cl30)