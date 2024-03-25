import telebot
from telebot import types
import pymysql
import os
import json
# from price import get_data

from config import TOKEN, HOST, USER, PASSWORD, PORT, DATABASE

bot = telebot.TeleBot(TOKEN)

connection = pymysql.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    port=PORT,
    database=DATABASE
)
cursor = connection.cursor()

# Про анотації розписав у функції start

phone = None
_id = None
_answer = None
current_index1 = 0
current_index2 = 0

# @bot.message_handler(commands=['update'])
# def update(message: str) -> None:
#     if message.chat.id != 163616716:
#         bot.send_message(message.chat.id, 'У Вас недостатньо повноважень для застосування цієї команди')
#     else:
#         get_data()
#         bot.send_message(message.chat.id, 'Ціни оновлено успішно')

def start_buttons() -> types.InlineKeyboardMarkup:
    """
    Це початкові кнопки, якщо треба детальне пояснення кнопок, що, як і куди працює, я поясню, або напишу тут
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    women = types.InlineKeyboardButton('🙋🏻‍♀️ Жіночі товари', callback_data = 'women')
    men = types.InlineKeyboardButton('🙋🏻‍♂️ Чоловічі товари', callback_data = 'men')
    help = types.InlineKeyboardButton('🛟 Отримати допомогу', callback_data = 'help')
    markup.add(women, men, help)
    return markup

def help_buttonts() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    back = types.InlineKeyboardButton('◀️ Назад', callback_data = 'help_back')
    home = types.InlineKeyboardButton('⏪ Головне меню', callback_data = 'help_home')
    markup.add(back, home)
    return markup

#функція, що поверає кнопки з жіночими товарами
def women_goods() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    back = types.InlineKeyboardButton('◀️ Назад', callback_data='back')
    home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home')
    # bags = types.InlineKeyboardButton('Сумки', callback_data='bags')
    big = types.InlineKeyboardButton('Вмісткі сумки', callback_data = 'big')
    small = types.InlineKeyboardButton('Компактні сумки', callback_data = 'small')
    backpacks = types.InlineKeyboardButton('Рюкзаки', callback_data='backpacks')
    accessories = types.InlineKeyboardButton('Аксесуари', callback_data='accessories_women')
    help = types.InlineKeyboardButton('🛟 Отримати допомогу', callback_data='help')
    markup.add(back, home, big, small, backpacks, accessories)
    markup.add(help)
    return markup

    # return bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Вами було обрано «🙋🏻‍♀️Жіночі товари», який товар Вас цікавить?\nОберіть категорію:', reply_markup=markup)


#функція, що поверає кнопки з чоловічими товарами
def men_goods() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    back = types.InlineKeyboardButton('◀️ Назад', callback_data = 'back')
    home = types.InlineKeyboardButton('⏪ Головне меню', callback_data = 'home')
    jacket = types.InlineKeyboardButton('Куртки', callback_data = 'jacket')
    pants = types.InlineKeyboardButton('Штани', callback_data = 'pants')
    accessories = types.InlineKeyboardButton('Аксесуари', callback_data = 'accessories_men')
    help = types.InlineKeyboardButton('🛟 Отримати допомогу', callback_data = 'help')
    markup.add(back, home, jacket, pants)
    markup.add(accessories)
    markup.add(help)

    return markup

#функція, що поверає кнопки з сумками
# def bags() -> types.InlineKeyboardMarkup:
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     back = types.InlineKeyboardButton('◀️ Назад', callback_data = 'back_bags')
#     home = types.InlineKeyboardButton('⏪ Головне меню', callback_data = 'home')
#     big = types.InlineKeyboardButton('Вмісткі сумки', callback_data = 'big')
#     small = types.InlineKeyboardButton('Компактні сумки', callback_data = 'small')
#     help = types.InlineKeyboardButton('🛟 Отримати допомогу', callback_data = 'help')
#     markup.add(back, home, big, small)
#     markup.add(help)
#     return markup

def help() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    home = types.InlineKeyboardButton('⏪ Головне меню', callback_data = 'home')
    q1 = types.InlineKeyboardButton('Як замовити?', callback_data = 'q1')
    q2 = types.InlineKeyboardButton('Коли та як оплатити за товар?', callback_data = 'q2')
    q3 = types.InlineKeyboardButton('Який час доставки товару?', callback_data = 'q3')
    q4 = types.InlineKeyboardButton('Обмін/Повернення товару', callback_data = 'q4')
    help_specialist = types.InlineKeyboardButton('Отримати допомогу фахівця', callback_data = 'help_specialist')
    markup.add(home)
    markup.add(q1, q2, q3, q4)
    markup.add(help_specialist)
    return markup

def help_one_more() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    home = types.InlineKeyboardButton('⏪ Головне меню', callback_data = 'home2')
    help = types.InlineKeyboardButton('❓ Спитатись ще', callback_data = 'help_specialist')
    markup.add(home, help)
    return markup

def q_handler(message):
    cht = message.chat.id

    if message.photo:
        photo_id = message.photo[-1].file_id
        caption = message.caption if message.caption else ''
        bot.send_photo(163616716, photo_id,
                    caption=f'id: <b>{cht}</b>\n'
                            f'name: {message.from_user.first_name} {message.from_user.last_name}\n'
                            f'username: <b>@{message.from_user.username}</b>\n'
                            f'phone: <b>{phone}</b>\n'
                            f'question: <b>{caption}</b>\n'
                            f'/answer', parse_mode='HTML')

    elif message.video:
        video_id = message.video.file_id
        caption = message.caption if message.caption else ''
        bot.send_video(163616716, video_id,
                    caption=f'id: <b>{cht}</b>\n'
                            f'name: {message.from_user.first_name} {message.from_user.last_name}\n'
                            f'username: <b>@{message.from_user.username}</b>\n'
                            f'phone: <b>{phone}</b>\n'
                            f'question: <b>{caption}</b>\n'
                            f'/answer', parse_mode='HTML')

    elif message.voice:
        voice_id = message.voice.file_id
        bot.send_voice(163616716, voice_id,
                       caption=f'id: <b>{cht}</b>\n'
                               f'name: {message.from_user.first_name} {message.from_user.last_name}\n'
                               f'username: <b>@{message.from_user.username}</b>\n'
                               f'phone: <b>{phone}</b>\n'
                               f'question: <b>{message.text}</b>\n'
                               f'/answer', parse_mode='HTML')
    else:
        bot.send_message(163616716, f'id: <b>{cht}</b>\n'
                                     f'name: {message.from_user.first_name} {message.from_user.last_name}\n'
                                     f'username: <b>@{message.from_user.username}</b>\n'
                                     f'phone: <b>{phone}</b>\n'
                                     f'question: <b>{message.text}</b>\n'
                                     f'/answer', parse_mode='HTML')

def answer_handler(message: str) -> None:
    cht = message.chat.id
    global _id

    _id = message.text

    msg = bot.send_message(cht, 'write answer/send photo/video:')
    bot.register_next_step_handler(msg, answer_send)

def answer_send(message: str) -> None:
    cht = message.chat.id
    global _answer

    if message.text:
        _answer = message.text
        try:
            bot.send_message(cht, f'Відповідь надіслано користувачу')
            bot.send_message(_id, f'✉️ Відповідь від менеджера вже тут!\nЗ радістю надаємо Вам відповідь від менеджера:\n<blockquote><b>{_answer}</b></blockquote>', parse_mode='HTML', reply_markup=help_one_more())
        except Exception as ex:
            bot.send_message(cht, f'Помилка\n{ex}')
            
    if message.photo:
        if message.caption:
            caption = message.caption
        else:
            caption = ''
            
        file_id = message.photo[-1].file_id
        try:
            bot.send_message(cht, f'Відповідь надіслано користувачу')
            bot.send_message(_id, f'✉️ Відповідь від менеджера вже тут!\nЗ радістю надаємо Вам відповідь від менеджера:')
            bot.send_photo(_id, file_id, caption=caption, reply_markup=help_one_more())
        except Exception as ex:
            bot.send_message(cht, f'Помилка надсилання фото\n{ex}')
            
    if message.video:
        if message.caption:
            caption = message.caption
        else:
            caption = ''
            
        file_id = message.video.file_id
        try:
            bot.send_message(cht, f'Відповідь надіслано користувачу')
            bot.send_message(_id, f'✉️ Відповідь від менеджера вже тут!\nЗ радістю надаємо Вам відповідь від менеджера:')
            bot.send_video(_id, file_id, caption=caption, reply_markup=help_one_more())
        except Exception as ex:
            bot.send_message(cht, f'Помилка надсилання відео\n{ex}')



def discount1(message):
    cht = message.chat.id

    if message.text == 'women':  
        sex = 'women'
        items = ''
        with open('items.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data['items'][sex]:
                items += f'{i}\n'
        msg = bot.send_message(cht, items)
        bot.register_next_step_handler(msg, discount2, sex)
    elif message.text == 'men': 
        sex = 'men'
        items = ''
        with open('items.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data['items'][sex]:
                items += f'{i}\n'
        msg = bot.send_message(cht, items)
        bot.register_next_step_handler(msg, discount2, sex)
    else:
        msg = bot.send_message(cht, 'спробуй ще раз')
        bot.register_next_step_handler(msg, discount1)

def discount2(message, sex):
    cht = message.chat.id
    group = message.text

    if message.text: 
        try: 
            items = ''
            with open('items.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for i in data['items'][sex][group]:
                    items += f'{i}\n'
            msg = bot.send_message(cht, items)
            bot.register_next_step_handler(msg, discount3, sex, group)
        except Exception as ex:
            msg = bot.send_message(cht, 'спробуй ще раз')
            bot.register_next_step_handler(msg, discount2, sex)
    else:
        msg = bot.send_message(cht, 'спробуй ще раз')
        bot.register_next_step_handler(msg, discount2, sex)

def discount3(message, sex, group):
    cht = message.chat.id
    item = message.text

    if message.text: 
        try: 
            items = ''
            with open('items.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for i in data['items'][sex][group][item]:
                    items += f'{i}\n'
            msg = bot.send_message(cht, 'Змінити текст? y/n')
            bot.register_next_step_handler(msg, discount4, sex, group, item)
        except Exception as ex:
            msg = bot.send_message(cht, 'спробуй ще раз')
            bot.register_next_step_handler(msg, discount3, sex)
    else:
        msg = bot.send_message(cht, 'спробуй ще раз')
        bot.register_next_step_handler(msg, discount3, sex)

def discount4(message, sex, group, item):
    cht = message.chat.id

    if message.text == 'y':
        msg = bot.send_message(cht, 'Напиши власний текст')
        bot.register_next_step_handler(msg, own_text, sex, group, item)
    elif message.text == 'n':
        with open('items.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            _data = data['items'][sex][group][item]

            image_path = _data['image_path']
            name_ = item
            old_price = _data['oldprice']
            new_price = _data['newprice']
            description = _data['description']
            url = _data['url']

            markup = types.InlineKeyboardMarkup(row_width=3)
            
            back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
            home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
            url = types.InlineKeyboardButton('🛒', url=f'{url}')
            markup.add(url)
            markup.add(back, home)
            
            cursor.execute("SELECT chat_id FROM users")
            ids = cursor.fetchall()
            for i in ids:
                bot.send_photo(i[0], open(os.path.join(image_path), 'rb'),
                                                caption=f'<b>{name_}</b>\n' +
                                                f'<s><i>{old_price} грн</i></s> <b>{new_price} грн</b>\n' +
                                                f'<blockquote>{description}</blockquote>',
                                                reply_markup=markup,
                                                parse_mode='HTML')

def own_text(message, sex, group, item):
    cht = message.chat.id

    with open('items.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        _data = data['items'][sex][group][item]

        image_path = _data['image_path']
        name_ = item
        old_price = _data['oldprice']
        new_price = _data['newprice']
        description = _data['description']
        url = _data['url']

        markup = types.InlineKeyboardMarkup(row_width=3)
            
        back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
        home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
        url = types.InlineKeyboardButton('🛒', url=f'{url}')
        markup.add(url)
        markup.add(back, home)
            
        cursor.execute("SELECT chat_id FROM users")
        ids = cursor.fetchall()
        for i in ids:
            bot.send_photo(i[0], open(os.path.join(image_path), 'rb'),
                                            caption = f'{message.text}\n\n' +
                                            f'<b>{name_}</b>\n' +
                                            f'<s><i>{old_price} грн</i></s> <b>{new_price} грн</b>\n' +
                                            f'<blockquote>{description}</blockquote>',
                                            reply_markup=markup,
                                            parse_mode='HTML')

# def send_discount(message, sex, sub_group):
#     cht = message.chat.id
#     name_ = message.text

#     try:
#         goods_items = open('items.json', 'r', encoding='utf-8')
#         data = json.load(goods_items)

#         description = data["items"][sex][sub_group][name_]["description"]
#         old_price = data["items"][sex][sub_group][name_]["oldprice"]
#         new_price = data["items"][sex][sub_group][name_]["newprice"]
#         image_path = data["items"][sex][sub_group][name_]["image_path"]
#         url = data["items"][sex][sub_group][name_]["url"]

#         markup = types.InlineKeyboardMarkup(row_width=3)
            
#         back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
#         home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
#         url = types.InlineKeyboardButton('🛒', url=f'{url}')
#         markup.add(url)
#         markup.add(back, home)
        
#         cursor.execute("SELECT chat_id FROM users")
#         data = cursor.fetchall()
#         print(data)
#         for i in data[0]:
#             bot.send_photo(i[0], open(os.path.join(image_path), 'rb'),
#                                         caption=f'⚠️ <b>{name_}</b>\n' +
#                                         f'<s><i>{old_price} грн</i></s> <b>{new_price} грн</b>\n\n' +
#                                         <blockquote>{description}</blockquote>',
#                                         reply_markup=markup,
#                                         parse_mode='HTML')
#     except Exception as ex:
#         bot.send_message(cht, 'Помилка! Погано введена група/підгрупа/товар')


#------------------------------------------------------------------------------------------------------------------------------

# Ця callback штука відповідає за вивід товарів
@bot.callback_query_handler(func=lambda call: call.data in ['back_j', 'next_j'])
def jacket_show(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        with open('prices.json', 'r', encoding='utf-8') as f2:
            data = json.load(f)
            data2 = json.load(f2)

            category = 'men'
            item_type = 'jacket'

            item_list = list(data['items'][category][item_type].keys())

            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            if call.data == 'back_j':
                current_index1 = (current_index1 - 1) % len(item_list)
            elif call.data == 'next_j':
                current_index1 = (current_index1 + 1) % len(item_list)

            t = item_list[current_index1]

            markup = types.InlineKeyboardMarkup(row_width=3)

            back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
            home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
            back_item = types.InlineKeyboardButton('◀️', callback_data='back_j')
            next_btn = types.InlineKeyboardButton('▶️', callback_data='next_j')
            url = types.InlineKeyboardButton('🛒', url=data['items'][category][item_type][t]['url'])
            markup.add(back_item, url, next_btn)
            markup.add(back, home)

            description = data2[t]['description']
            old_price = data2[t]['oldprice']
            new_price = data2[t]['newprice']
            image_path = data['items'][category][item_type][t]['image_path']

            caption = f'<b>{t}</b>\n'
            if old_price == new_price:
                caption += f'<blockquote>{description}</blockquote>\n{new_price}'
            else:
                caption += f'<s><i>{old_price} грн</i></s> <b>{new_price} грн</b>\n<blockquote>{description}</blockquote>'

            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=caption,
                           reply_markup=markup,
                           parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data in ['bp', 'np'])
def pants_show(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        with open('prices.json', 'r', encoding='utf-8') as f2:
            data = json.load(f)
            data2 = json.load(f2)

            category = 'men'
            item_type = 'pants'

            item_list = list(data['items'][category][item_type].keys())

            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            if call.data == 'bp':
                current_index1 = (current_index1 - 1) % len(item_list)
            elif call.data == 'bp':
                current_index1 = (current_index1 + 1) % len(item_list)

            t = item_list[current_index1]

            markup = types.InlineKeyboardMarkup(row_width=3)

            back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
            home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
            back_item = types.InlineKeyboardButton('◀️', callback_data='bp')
            next_btn = types.InlineKeyboardButton('▶️', callback_data='bp')
            url = types.InlineKeyboardButton('🛒', url=data['items'][category][item_type][t]['url'])
            markup.add(back_item, url, next_btn)
            markup.add(back, home)

            description = data2[t]['description']
            old_price = data2[t]['oldprice']
            new_price = data2[t]['newprice']
            image_path = data['items'][category][item_type][t]['image_path']

            caption = f'<b>{t}</b>\n'
            if old_price == new_price:
                caption += f'<blockquote>{description}</blockquote>\n{new_price}'
            else:
                caption += f'<s><i>{old_price} грн</i></s> <b>{new_price} грн</b>\n<blockquote>{description}</blockquote>'

            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=caption,
                           reply_markup=markup,
                           parse_mode='HTML')
        
@bot.callback_query_handler(func=lambda call: call.data in ['bac', 'nac'])
def accessories_men(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        with open('prices.json', 'r', encoding='utf-8') as f2:
            data = json.load(f)
            data2 = json.load(f2)

            category = 'men'
            item_type = 'accessories_men'

            item_list = list(data['items'][category][item_type].keys())

            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            if call.data == 'bac':
                current_index1 = (current_index1 - 1) % len(item_list)
            elif call.data == 'nac':
                current_index1 = (current_index1 + 1) % len(item_list)

            t = item_list[current_index1]

            markup = types.InlineKeyboardMarkup(row_width=3)

            back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
            home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
            back_item = types.InlineKeyboardButton('◀️', callback_data='bac')
            next_btn = types.InlineKeyboardButton('▶️', callback_data='nac')
            url = types.InlineKeyboardButton('🛒', url=data['items'][category][item_type][t]['url'])
            markup.add(back_item, url, next_btn)
            markup.add(back, home)

            description = data2[t]['description']
            old_price = data2[t]['oldprice']
            new_price = data2[t]['newprice']
            image_path = data['items'][category][item_type][t]['image_path']

            caption = f'<b>{t}</b>\n'
            if old_price == new_price:
                caption += f'<blockquote>{description}</blockquote>\n{new_price}'
            else:
                caption += f'<s><i>{old_price} грн</i></s> <b>{new_price} грн</b>\n<blockquote>{description}</blockquote>'

            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=caption,
                           reply_markup=markup,
                           parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data in ['bbb', 'bbn'])
def big_bags(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        with open('prices.json', 'r', encoding='utf-8') as f2:
            data = json.load(f)
            data2 = json.load(f2)

            category = 'women'
            item_type = 'big.bags'

            item_list = list(data['items'][category][item_type].keys())

            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            if call.data == 'bbb':
                current_index1 = (current_index1 - 1) % len(item_list)
            elif call.data == 'bbn':
                current_index1 = (current_index1 + 1) % len(item_list)

            t = item_list[current_index1]

            markup = types.InlineKeyboardMarkup(row_width=3)

            back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
            home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
            back_item = types.InlineKeyboardButton('◀️', callback_data='bbb')
            next_btn = types.InlineKeyboardButton('▶️', callback_data='bbn')
            url = types.InlineKeyboardButton('🛒', url=data['items'][category][item_type][t]['url'])
            markup.add(back_item, url, next_btn)
            markup.add(back, home)

            description = data2[t]['description']
            old_price = data2[t]['oldprice']
            new_price = data2[t]['newprice']
            image_path = data['items'][category][item_type][t]['image_path']

            caption = f'<b>{t}</b>\n'
            if old_price == new_price:
                caption += f'<blockquote>{description}</blockquote>\n{new_price}'
            else:
                caption += f'<s><i>{old_price} грн</i></s> <b>{new_price} грн</b>\n<blockquote>{description}</blockquote>'

            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=caption,
                           reply_markup=markup,
                           parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data in ['sbb', 'sbn'])
def small_bags(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        with open('prices.json', 'r', encoding='utf-8') as f2:
            data = json.load(f)
            data2 = json.load(f2)

            category = 'women'
            item_type = 'small.bags'

            item_list = list(data['items'][category][item_type].keys())

            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            if call.data == 'sbb':
                current_index1 = (current_index1 - 1) % len(item_list)
            elif call.data == 'sbn':
                current_index1 = (current_index1 + 1) % len(item_list)

            t = item_list[current_index1]

            markup = types.InlineKeyboardMarkup(row_width=3)

            back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
            home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
            back_item = types.InlineKeyboardButton('◀️', callback_data='sbb')
            next_btn = types.InlineKeyboardButton('▶️', callback_data='sbn')
            url = types.InlineKeyboardButton('🛒', url=data['items'][category][item_type][t]['url'])
            markup.add(back_item, url, next_btn)
            markup.add(back, home)

            description = data2[t]['description']
            old_price = data2[t]['oldprice']
            new_price = data2[t]['newprice']
            image_path = data['items'][category][item_type][t]['image_path']

            caption = f'<b>{t}</b>\n'
            if old_price == new_price:
                caption += f'<blockquote>{description}</blockquote>\n{new_price}'
            else:
                caption += f'<s><i>{old_price} грн</i></s> <b>{new_price} грн</b>\n<blockquote>{description}</blockquote>'

            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=caption,
                           reply_markup=markup,
                           parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data in ['bb', 'bn'])
def backpack(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        with open('prices.json', 'r', encoding='utf-8') as f2:
            data = json.load(f)
            data2 = json.load(f2)

            category = 'women'
            item_type = 'backpack'

            item_list = list(data['items'][category][item_type].keys())

            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            if call.data == 'bb':
                current_index1 = (current_index1 - 1) % len(item_list)
            elif call.data == 'bn':
                current_index1 = (current_index1 + 1) % len(item_list)

            t = item_list[current_index1]

            markup = types.InlineKeyboardMarkup(row_width=3)

            back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
            home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
            back_item = types.InlineKeyboardButton('◀️', callback_data='bb')
            next_btn = types.InlineKeyboardButton('▶️', callback_data='bn')
            url = types.InlineKeyboardButton('🛒', url=data['items'][category][item_type][t]['url'])
            markup.add(back_item, url, next_btn)
            markup.add(back, home)

            description = data2[t]['description']
            old_price = data2[t]['oldprice']
            new_price = data2[t]['newprice']
            image_path = data['items'][category][item_type][t]['image_path']

            caption = f'<b>{t}</b>\n'
            if old_price == new_price:
                caption += f'<blockquote>{description}</blockquote>\n{new_price}'
            else:
                caption += f'<s><i>{old_price} грн</i></s> <b>{new_price} грн</b>\n<blockquote>{description}</blockquote>'

            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=caption,
                           reply_markup=markup,
                           parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data in ['awb', 'awn'])
def accessories_women(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        with open('prices.json', 'r', encoding='utf-8') as f2:
            data = json.load(f)
            data2 = json.load(f2)

            category = 'women'
            item_type = 'accessories_women'

            item_list = list(data['items'][category][item_type].keys())

            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            if call.data == 'awb':
                current_index1 = (current_index1 - 1) % len(item_list)
            elif call.data == 'awn':
                current_index1 = (current_index1 + 1) % len(item_list)

            t = item_list[current_index1]

            markup = types.InlineKeyboardMarkup(row_width=3)

            back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
            home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
            back_item = types.InlineKeyboardButton('◀️', callback_data='awb')
            next_btn = types.InlineKeyboardButton('▶️', callback_data='awn')
            url = types.InlineKeyboardButton('🛒', url=data['items'][category][item_type][t]['url'])
            markup.add(back_item, url, next_btn)
            markup.add(back, home)

            description = data2[t]['description']
            old_price = data2[t]['oldprice']
            new_price = data2[t]['newprice']
            image_path = data['items'][category][item_type][t]['image_path']

            caption = f'<b>{t}</b>\n'
            if old_price == new_price:
                caption += f'<blockquote>{description}</blockquote>\n{new_price}'
            else:
                caption += f'<s><i>{old_price} грн</i></s> <b>{new_price} грн</b>\n<blockquote>{description}</blockquote>'

            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=caption,
                           reply_markup=markup,
                           parse_mode='HTML')




#------------------------------------------------------------------------------------------------------------------------------

# обробник команди /start
@bot.message_handler(commands=['start', 'goods_list'])
def start(message: str) -> None:
    """
    (message: str) - то анотація, вказуємо тип даних аргументу message
    (-> None) - тут ми вкауємо, що функція нічого не повертає
    """
    cht = message.chat.id

    cursor.execute("CREATE TABLE IF NOT EXISTS users (id int AUTO_INCREMENT, chat_id varchar(10), PRIMARY KEY(id))")
    connection.commit()
    cursor.execute("SELECT * FROM users WHERE chat_id = %s", (cht,))
    existing_user = cursor.fetchone()

    # Якщо запис не знайдено, то вставляємо новий запис
    if not existing_user:
        cursor.execute("INSERT INTO users (chat_id) VALUES (%s)", (cht,))
        connection.commit()

    bot.send_message(cht, 'Вітаємо у магазині 6bags\nДля навігації по магазину, оберіть категорію:', reply_markup=start_buttons())

@bot.message_handler(commands=['answer'])
def answer(message: str) -> None:
    cht = message.chat.id

    if cht != 163616716:
        bot.send_message(cht, 'У Вас недостатньо повноважень для застосування цієї команди')
    else:
        msg = bot.send_message(cht, 'id:')
        bot.register_next_step_handler(msg, answer_handler)

@bot.message_handler(commands=['help'])
def goods_list(message: str) -> None:
    cht = message.chat.id

    bot.send_message(cht, 'Скористайтесь питаннями або задайте власне нашому менеджеру', reply_markup=help())

@bot.message_handler(commands=['send_discount'])
def discount_(message: str) -> None:
    cht = message.chat.id

    if cht != 163616716:
        bot.send_message(cht, 'У Вас недостатньо повноважень для застосування цієї команди')
    else:
        items = ''
        with open('items.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data['items']:
                items += f'{i}\n'
        msg = bot.send_message(cht, items)
        bot.register_next_step_handler(msg, discount1)


# з цією штукою сам до кінця не розібрався( Воно треба для обробки інлайнових кнопок
@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    cht = call.message.chat.id

    # тут ми перевіряємо, на яку кнопку тицьнув користувач
    if call.message:
        if call.data == 'women':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Вами було обрано «🙋🏻‍♀️Жіночі товари», який товар Вас цікавить?\nОберіть категорію:', reply_markup=women_goods())
        if call.data == 'men':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Вами було обрано «🙋🏻‍♂️Чоловічі товари», який товар Вас цікавить?\nОберіть категорію:', reply_markup=men_goods())
        elif call.data == 'big':
            big_bags(call)
        elif call.data == 'small':
            small_bags(call)
        elif call.data == 'backpacks':
            backpack(call)
        elif call.data == 'accessories_women':
            accessories_women(call)
        elif call.data == 'help':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Скористайтесь питаннями або задайте власне нашому менеджеру', reply_markup=help())
        elif call.data == 'jacket':
            jacket_show(call)
        elif call.data == 'pants':
            pants_show(call)
        elif call.data == 'accessories_men':
            accessories_men(call)
         

        elif call.data == 'back_btn_men':
            bot.send_message(cht, 'Вами було обрано «🙋🏻‍♂️Чоловічі товари», який товар Вас цікавить?\nОберіть категорію:', reply_markup=men_goods())
        elif call.data == 'home_btn_men':
            bot.send_message(cht, 'Вітаємо у магазині 6bags\nДля навігації по магазину, оберіть категорію:', reply_markup=start_buttons())
        elif call.data == 'back_btn_women':
            bot.send_message(cht, 'Вами було обрано «🙋🏻‍♀️Жіночі товари», який товар Вас цікавить?\nОберіть категорію:', reply_markup=women_goods())

        # elif call.data == 'back_btn_women':
        #     bot.send_message(cht, 'Сумки:', reply_markup=bags())
        #     women_goods(call=call)
        # elif call.data == 'back_btn_women':
        #     women_goods(call=call)
        elif call.data == 'home_btn_women':
            bot.send_message(cht, 'Вітаємо у магазині 6bags\nДля навігації по магазину, оберіть категорію:', reply_markup=start_buttons())




        elif call.data == 'q1':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id,
                                  text="""1. Оберіть товар, який бажаєте замовити, та натисніть «🛒» для відкриття картки товару
2. Замовлення - Залишаєте заявку на нашому сайті
3. Дзвінок - Наш менеджер уточнює деталі замовлення
4. Відправка - Доставляємо товар протягом 1-3 днів
5. Отримання - Оплачуєте при отриманні на пошті.""",
                                  reply_markup=help_buttonts())
        elif call.data == 'q2':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id,
                                  text="""Оплата за товар може бути наступною:
Наложений платіж - після огляду товару на пошті.
Передоплата - оплачуєте наперід. В разі відмови, ми повернемо Вам кошти.""",
                                  reply_markup=help_buttonts())
        elif call.data == 'q3':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id,
                                  text="""Товар доставляється Вам протягом 1-3 днів в залежності від поштового перевізника якого Ви обрали (Нова Пошта - швидко; Укрпошта - дешево)""",
                                  reply_markup=help_buttonts())
        elif call.data == 'q4':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id,
                                  text="""Компанія здійснює повернення і обмін товарів належної якості згідно Закону <a href='https://zakon.rada.gov.ua/laws/show/1023-12#Text'>«Про захист прав споживачів»</a>.

Строки повернення і обміну
Повернення та обмін товарів можливий протягом 14 днів після отримання товару покупцем.

Зворотня доставка товарів здійснюється за домовленістю.

Умови повернення для товарів належної якості

Товари магазину 6bags підлягають обміну у разі незадоволеності клієнта покупкою. 
Для оформлення обміну ви повинні протягом 14 днів після покупки зв'язатися з магазином за телефоном 380501419080, повідомити та надіслати товар до магазину. 
Обмін товару здійснюється Новою поштою або Укрпоштою з оплатою поштових послуг за рахунок відправника. Новий товар з обміну надсилається клієнту наступного дня після отримання товару магазином через пошту. 

Товари магазину 6bags підлягають поверненню, у разі незадоволеності клієнта покупкою. 
Для оформлення повернення ви повинні протягом 14 днів після покупки зв'язатися з магазином за телефоном 380501419080, повідомити та надіслати товар до магазину. 
Повернення товару здійснюється Новою поштою або Укрпоштою з оплатою поштових послуг за рахунок відправника. Повернення грошей здійснюється на картку клієнта наступного дня після отримання товару магазином через пошту.

Відповідно закону <a href='https://zakon.rada.gov.ua/laws/show/1023-12#Text'>«Про захист прав споживачів»</a>, компанія може відмовити споживачеві в обміні та поверненні товарів належної якості, якщо вони відносяться до категорій, зазначених у чинному <a href='https://zakon.rada.gov.ua/laws/show/172-94-%D0%BF#Text'>Переліку непродовольчих товарів належної якості, що не підлягають поверненню та обміну</a>.""",
                                  reply_markup=help_buttonts(),
                                  parse_mode='HTML')
        elif call.data == 'help_specialist':
            global phone

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            phone = types.KeyboardButton('Надіслати контакт', request_contact=True)
            markup.add(phone)
            bot.send_message(cht, 'Надішліть контакт', reply_markup=markup)


        # Ці блоки elif відокремлені, бо тут ціла система повернень назад :)
        elif call.data == 'back':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Вітаємо у магазині 6bags\nДля навігації по магазину, оберіть категорію:', reply_markup=start_buttons())
        elif call.data == 'back_bags':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Вами було обрано «🙋🏻‍♀️Жіночі товари», який товар Вас цікавить?\nОберіть категорію:', reply_markup=women_goods())
        elif call.data == 'home':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Вітаємо у магазині 6bags\nДля навігації по магазину, оберіть категорію:', reply_markup=start_buttons())
        elif call.data == 'home2':
            bot.send_message(cht, 'Вітаємо у магазині 6bags\nДля навігації по магазину, оберіть категорію:', reply_markup=start_buttons())

        elif call.data == 'help_back':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Скористайтесь питаннями або задайте власне нашому менеджеру', reply_markup=help())
        elif call.data == 'help_home':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Вітаємо у магазині 6bags\nДля навігації по магазину, оберіть категорію:', reply_markup=start_buttons())



# обробник тексту
@bot.message_handler(content_types=['contact'])
def text(message):
    cht = message.chat.id
    global phone

    if message.contact:
        phone = message.contact.phone_number

        keyboard = types.ReplyKeyboardRemove()
        msg = bot.send_message(cht, 'Надішліть питання', reply_markup=keyboard)

        bot.register_next_step_handler(msg, q_handler)

bot.polling()