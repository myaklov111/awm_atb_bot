from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


main_menu=ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Управление'),
         ],

        [
            KeyboardButton(text='Настройки'),
            KeyboardButton(text='Помощь'),
         ],

    ],
    resize_keyboard=True
)

main_menu_control=ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Старт'),
         ],
[
            KeyboardButton(text='Стоп'),
         ],

        [
            KeyboardButton(text='Назад'),
         ],

    ],
    resize_keyboard=True
)




settings_menu=ReplyKeyboardMarkup(
    [

        [
            KeyboardButton(text='Добавить ссылку'),

         ],
        [
            KeyboardButton(text='Настройка времени')
        ],
        [
            KeyboardButton(text='Назад')
        ]

    ],
    resize_keyboard=True
)


back_menu=ReplyKeyboardMarkup(
    [

        [
            KeyboardButton(text='Назад')
        ]

    ],
    resize_keyboard=True
)


set_time_menu=ReplyKeyboardMarkup(
    [

        [
            KeyboardButton(text='Установить время'),

         ],
        [
            KeyboardButton(text='Назад')
        ]

    ],
    resize_keyboard=True
)
