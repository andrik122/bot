import telebot
from telebot import types
import os
import json
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# Про анотації розписав у функції start

phone = None
_id = None
_answer = None
current_index1 = 0
current_index2 = 0

def start_buttons() -> types.InlineKeyboardMarkup:
    """
    Це початкові кнопки, якщо треба детальне пояснення кнопок, що, як і куди працює, я поясню, або напишу тут
    """
    markup = types.InlineKeyboardMarkup(row_width=2)
    women = types.InlineKeyboardButton('🙋‍♀️ Жіночі товари', callback_data = 'women')
    men = types.InlineKeyboardButton('🙋‍♂️ Чоловічі товари', callback_data = 'men')
    help = types.InlineKeyboardButton('🛟 Отримати допомогу', callback_data = 'help')
    markup.add(women, men, help)
    return markup

#функція, що поверає кнопки з жіночими товарами
def women_goods(call) -> types.InlineKeyboardMarkup:
    cht= call.message.chat.id

    markup = types.InlineKeyboardMarkup(row_width=2)
    back = types.InlineKeyboardButton('◀️ Назад', callback_data = 'back')
    home = types.InlineKeyboardButton('⏪ Головне меню', callback_data = 'home')
    bags = types.InlineKeyboardButton('Сумки', callback_data = 'bags')
    backpacks = types.InlineKeyboardButton('Рюкзаки', callback_data = 'backpacks')
    accessories = types.InlineKeyboardButton('Аксесуари', callback_data = 'accessories_women')
    help = types.InlineKeyboardButton('🛟 Отримати допомогу', callback_data = 'help')
    markup.add(back, home, bags, backpacks)
    markup.add(accessories)
    markup.add(help)

    return bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Ви обрали жіночі товари', reply_markup=markup)

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
def bags() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    back = types.InlineKeyboardButton('◀️ Назад', callback_data = 'back_bags')
    home = types.InlineKeyboardButton('⏪ Головне меню', callback_data = 'home')
    big = types.InlineKeyboardButton('Вмісткі сумки', callback_data = 'big')
    small = types.InlineKeyboardButton('Компактні сумки', callback_data = 'small')
    help = types.InlineKeyboardButton('🛟 Отримати допомогу', callback_data = 'help')
    markup.add(back, home, big, small)
    markup.add(help)
    return markup

def help() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    home = types.InlineKeyboardButton('⏪ Головне меню', callback_data = 'home')
    q1 = types.InlineKeyboardButton('Питання 1', callback_data = 'q1')
    q2 = types.InlineKeyboardButton('Питання 2', callback_data = 'q2')
    q3 = types.InlineKeyboardButton('Питання 3', callback_data = 'q3')
    q4 = types.InlineKeyboardButton('Питання 4', callback_data = 'q4')
    help_specialist = types.InlineKeyboardButton('Отримати допомогу фахівця', callback_data = 'help_specialist')
    markup.add(home)
    markup.add(q1, q2, q3, q4)
    markup.add(help_specialist)
    return markup

def help_one_more() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=2)
    home = types.InlineKeyboardButton('⏪ Головне меню', callback_data = 'home')
    help = types.InlineKeyboardButton('❓ Спитатись ще', callback_data = 'help_specialist')
    markup.add(home, help)
    return markup

def q_handler(message: str) -> None:
    cht = message.chat.id

    bot.send_message(cht, 'Менеджер вже поспішає надати відповідь ⌛️\nА поки, можете переглянути наші товари ☺️', reply_markup=start_buttons())
    bot.send_message(1001173176, f'id: <b>{cht}</b>\nusername: <b>@{message.from_user.username}</b>\nphone: <b>{phone}</b>\nquestion: <b>{message.text}</b>', parse_mode='HTML')

def answer_handler(message: str) -> None:
    cht = message.chat.id
    global _id

    _id = message.text

    msg = bot.send_message(cht, 'write answer:')
    bot.register_next_step_handler(msg, answer_send)

def answer_send(message: str) -> None:
    cht = message.chat.id
    global _answer

    _answer = message.text

    try:
        bot.send_message(cht, f'Відповідь надіслано користувачу')
        bot.send_message(_id, f'Вам надішла відповідь від менеджера:\n<b><i>{_answer}</i></b>', parse_mode='HTML', reply_markup=help_one_more())
        # bot.send_message(_id, f'Щоб надіслати питання ще раз, скористайтесь кнопкою', reply_markup=help_one_more())
    except Exception as ex:
        bot.send_message(cht, f'Помилка\n{ex}')

def send_discount(message: str) -> None:
    name_ = message.text

    goods_items = open('items.json', 'r', encoding='utf-8')
    data = json.load(goods_items)

    description1 = data["items"]['men']["jacket"][name_]["description1"]
    description2 = data["items"]['men']["jacket"][name_]["description2"]
    description3 = data["items"]['men']["jacket"][name_]["description3"]
    description4 = data["items"]['men']["jacket"][name_]["description4"]
    description5 = data["items"]['men']["jacket"][name_]["description5"]
    old_price = data["items"]['men']["jacket"][name_]["oldprice"]
    new_price = data["items"]['men']["jacket"][name_]["newprice"]
    image_path = data["items"]['men']["jacket"][name_]["image_path"]
    url = data["items"]['men']["jacket"][name_]["url"]

    markup = types.InlineKeyboardMarkup(row_width=3)
        
    back = types.InlineKeyboardButton('◀️ Назад', callback_data = 'back_btn_men')
    home = types.InlineKeyboardButton('⏪ Головне меню', callback_data = 'home_btn_men')
    url = types.InlineKeyboardButton('🛒', url=f'{url}')
    markup.add(url)
    markup.add(back, home)
 
    with open('users.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for i in data['chat_ids']:
            bot.send_photo(i, open(os.path.join(image_path), 'rb'),
                                    caption=f'⚠️ <b>{name_}</b>\n' +
                                    f'<s><i>{old_price}</i></s> <b>{new_price}</b>\n\n' +
                                    f'{description1}\n{description2}\n{description3}\n{description4}\n{description5}',
                                    reply_markup=markup,
                                    parse_mode='HTML')

#------------------------------------------------------------------------------------------------------------------------------

# Ця callback штука відповідає за вивід товарів
@bot.callback_query_handler(func=lambda call: call.data in ['back_j', 'next_j'])
def jacket_show(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        item_list = list(data['items']['men']['jacket'].keys())

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
        url = types.InlineKeyboardButton('🛒', url=data['items']['men']['jacket'][t]['url'])
        markup.add(back_item, url, next_btn)
        markup.add(back, home)

        description = '\n'.join(data["items"]['men']["jacket"][t][f"description{i}"] for i in range(1, 6))
        old_price = data["items"]['men']["jacket"][t]["oldprice"]
        new_price = data["items"]['men']["jacket"][t]["newprice"]
        image_path = data["items"]['men']["jacket"][t]["image_path"]

        caption = f'<b>{t}</b>\n'
        if old_price == new_price:
            caption += f'{description}\n{new_price}'
        else:
            caption += f'<s><i>₴{old_price}</i></s> <b>₴{new_price}</b>\n\n{description}'

        bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                       caption=caption,
                       reply_markup=markup,
                       parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data in ['bp', 'np'])
def pants_show(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        item_list = list(data['items']['men']['pants'].keys())

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if call.data == 'bp':
            current_index1 = (current_index1 - 1) % len(item_list)
        elif call.data == 'np':
            current_index1 = (current_index1 + 1) % len(item_list)

        # Переконайтеся, що список не порожній, перш ніж отримувати елемент за індексом
        if item_list:
            t = item_list[current_index1]

            markup = types.InlineKeyboardMarkup(row_width=3)

            back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_men')
            home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_men')
            back_item = types.InlineKeyboardButton('◀️', callback_data='bp')
            next_btn = types.InlineKeyboardButton('▶️', callback_data='np')
            url = types.InlineKeyboardButton('🛒', url=data['items']['men']['pants'][t]['url'])
            markup.add(back_item, url, next_btn)
            markup.add(back, home)

            description = '\n'.join(data["items"]['men']["pants"][t][f"description{i}"] for i in range(1, 6))
            old_price = data["items"]['men']["pants"][t]["oldprice"]
            new_price = data["items"]['men']["pants"][t]["newprice"]
            image_path = data["items"]['men']["pants"][t]["image_path"]

            caption = f'<b>{t}</b>\n'
            if old_price == new_price:
                caption += f'{description}\n{new_price}'
            else:
                caption += f'<s><i>₴{old_price}</i></s> <b>₴{new_price}</b>\n\n{description}'

            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=caption,
                           reply_markup=markup,
                           parse_mode='HTML')
        else:
            bot.send_message(call.message.chat.id, "Список елементів порожній")

    f.close()
        
@bot.callback_query_handler(func=lambda call: call.data in ['bac', 'nac'])
def accessories_men(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        item_list = list(data['items']['men']['accessories_men'].keys())

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
        url = types.InlineKeyboardButton('🛒', url=data['items']['men']['accessories_men'][t]['url'])
        markup.add(back_item, url, next_btn)
        markup.add(back, home)

        description1 = data["items"]['men']["accessories_men"][t]["description1"]
        old_price = data["items"]['men']["accessories_men"][t]["oldprice"]
        new_price = data["items"]['men']["accessories_men"][t]["newprice"]
        image_path = data["items"]['men']["accessories_men"][t]["image_path"]

        if old_price == new_price:    
            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=f'<b>{t}</b>\n{description1}{new_price}',
                           reply_markup=markup,
                           parse_mode='HTML')
        else:
            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=f'<b>{t}</b>\n<s><i>₴{old_price}</i></s> <b>₴{new_price}</b>\n\n{description1}',
                           reply_markup=markup,
                           parse_mode='HTML')
    f.close()


@bot.callback_query_handler(func=lambda call: call.data in ['bbb', 'bbn'])
def big_bags(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        item_list = list(data['items']['women']['bags']['big.bags'].keys())

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if call.data == 'bbb':
            current_index1 = (current_index1 - 1) % len(item_list)
        elif call.data == 'bbn':
            current_index1 = (current_index1 + 1) % len(item_list)

        t = item_list[current_index1]

        markup = types.InlineKeyboardMarkup(row_width=3)
        
        back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_women')
        home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_women')
        back_item = types.InlineKeyboardButton('◀️', callback_data='bbb')
        next_btn = types.InlineKeyboardButton('▶️', callback_data='bbn')
        url = types.InlineKeyboardButton('🛒', url=data['items']['women']['bags']['big.bags'][t]['url'])
        markup.add(back_item, url, next_btn)
        markup.add(back, home)

        description1 = data["items"]['women']['bags']["big.bags"][t]["description1"]
        description2 = data["items"]['women']['bags']["big.bags"][t]["description2"]
        description3 = data["items"]['women']['bags']["big.bags"][t]["description3"]
        description4 = data["items"]['women']['bags']["big.bags"][t]["description4"]
        description5 = data["items"]['women']['bags']["big.bags"][t]["description5"]
        old_price = data["items"]['women']['bags']["big.bags"][t]["oldprice"]
        new_price = data["items"]['women']['bags']["big.bags"][t]["newprice"]
        image_path = data["items"]['women']['bags']["big.bags"][t]["image_path"]

        if old_price == new_price:    
            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=f'<b>{t}</b>\n<b>₴{new_price}</b>\n\n{description1}\n{description2}\n{description3}\n{description4}\n{description5}',
                           reply_markup=markup,
                           parse_mode='HTML')
        else:
            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=f'<b>{t}</b>\n<s><i>₴{old_price}</i></s> <b>₴{new_price}</b>\n\n{description1}\n{description2}\n{description3}\n{description4}\n{description5}',
                           reply_markup=markup,
                           parse_mode='HTML')
    f.close()


@bot.callback_query_handler(func=lambda call: call.data in ['sbb', 'sbn'])
def small_bags(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        item_list = list(data['items']['women']['bags']['small.bags'].keys())

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if call.data == 'sbb':
            current_index1 = (current_index1 - 1) % len(item_list)
        elif call.data == 'sbn':
            current_index1 = (current_index1 + 1) % len(item_list)

        t = item_list[current_index1]

        markup = types.InlineKeyboardMarkup(row_width=3)
        
        back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_women')
        home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_women')
        back_item = types.InlineKeyboardButton('◀️', callback_data='sbb')
        next_btn = types.InlineKeyboardButton('▶️', callback_data='sbn')
        url = types.InlineKeyboardButton('🛒', url=data['items']['women']['bags']['small.bags'][t]['url'])
        markup.add(back_item, url, next_btn)
        markup.add(back, home)

        description1 = data["items"]['women']['bags']["small.bags"][t]["description1"]
        description2 = data["items"]['women']['bags']["small.bags"][t]["description2"]
        description3 = data["items"]['women']['bags']["small.bags"][t]["description3"]
        description4 = data["items"]['women']['bags']["small.bags"][t]["description4"]
        description5 = data["items"]['women']['bags']["small.bags"][t]["description5"]
        old_price = data["items"]['women']['bags']["small.bags"][t]["oldprice"]
        new_price = data["items"]['women']['bags']["small.bags"][t]["newprice"]
        image_path = data["items"]['women']['bags']["small.bags"][t]["image_path"]

        if old_price == new_price:    
            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=f'<b>{t}</b>\n<b>₴{new_price}</b>\n\n{description1}\n{description2}\n{description3}\n{description4}\n{description5}',
                           reply_markup=markup,
                           parse_mode='HTML')
        else:
            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=f'<b>{t}</b>\n<s><i>₴{old_price}</i></s> <b>₴{new_price}</b>\n\n{description1}\n{description2}\n{description3}\n{description4}\n{description5}',
                           reply_markup=markup,
                           parse_mode='HTML')
    f.close()


@bot.callback_query_handler(func=lambda call: call.data in ['bb', 'bn'])
def backpack(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        item_list = list(data['items']['women']['backpack'].keys())

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if call.data == 'bb':
            current_index1 = (current_index1 - 1) % len(item_list)
        elif call.data == 'bn':
            current_index1 = (current_index1 + 1) % len(item_list)

        t = item_list[current_index1]

        markup = types.InlineKeyboardMarkup(row_width=3)
        
        back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_women')
        home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_women')
        back_item = types.InlineKeyboardButton('◀️', callback_data='bb')
        next_btn = types.InlineKeyboardButton('▶️', callback_data='bn')
        url = types.InlineKeyboardButton('🛒', url=data['items']['women']['backpack'][t]['url'])
        markup.add(back_item, url, next_btn)
        markup.add(back, home)

        description1 = data["items"]['women']["backpack"][t]["description1"]
        description2 = data["items"]['women']["backpack"][t]["description2"]
        description3 = data["items"]['women']["backpack"][t]["description3"]
        description4 = data["items"]['women']["backpack"][t]["description4"]
        description5 = data["items"]['women']["backpack"][t]["description5"]
        old_price = data["items"]['women']["backpack"][t]["oldprice"]
        new_price = data["items"]['women']["backpack"][t]["newprice"]
        image_path = data["items"]['women']["backpack"][t]["image_path"]

        if old_price == new_price:    
            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=f'<b>{t}</b>\n<b>₴{new_price}</b>\n\n{description1}\n{description2}\n{description3}\n{description4}\n{description5}',
                           reply_markup=markup,
                           parse_mode='HTML')
        else:
            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=f'<b>{t}</b>\n<s><i>₴{old_price}</i></s> <b>₴{new_price}</b>\n\n{description1}\n{description2}\n{description3}\n{description4}\n{description5}',
                           reply_markup=markup,
                           parse_mode='HTML')
    f.close()


@bot.callback_query_handler(func=lambda call: call.data in ['awb', 'awn'])
def accessories_women(call):
    global current_index1

    with open('items.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        item_list = list(data['items']['women']['accessories_women'].keys())

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

        if call.data == 'awb':
            current_index1 = (current_index1 - 1) % len(item_list)
        elif call.data == 'awn':
            current_index1 = (current_index1 + 1) % len(item_list)

        t = item_list[current_index1]

        markup = types.InlineKeyboardMarkup(row_width=3)
        
        back = types.InlineKeyboardButton('◀️ Назад', callback_data='back_btn_women')
        home = types.InlineKeyboardButton('⏪ Головне меню', callback_data='home_btn_women')
        back_item = types.InlineKeyboardButton('◀️', callback_data='awb')
        next_btn = types.InlineKeyboardButton('▶️', callback_data='awn')
        url = types.InlineKeyboardButton('🛒', url=data['items']['women']['accessories_women'][t]['url'])
        markup.add(back_item, url, next_btn)
        markup.add(back, home)

        description1 = data["items"]['women']["accessories_women"][t]["description1"]
        # description2 = data["items"]['women']["accessories_women"][t]["description2"]
        # description3 = data["items"]['women']["accessories_women"][t]["description3"]
        # description4 = data["items"]['women']["accessories_women"][t]["description4"]
        # description5 = data["items"]['women']["accessories_women"][t]["description5"]
        old_price = data["items"]['women']["accessories_women"][t]["oldprice"]
        new_price = data["items"]['women']["accessories_women"][t]["newprice"]
        image_path = data["items"]['women']["accessories_women"][t]["image_path"]

        if old_price == new_price:    
            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=f'<b>{t}</b>\n{description1}\n<b>₴{new_price}</b>',
                           reply_markup=markup,
                           parse_mode='HTML')
        else:
            bot.send_photo(call.message.chat.id, open(os.path.join(image_path), 'rb'),
                           caption=f'<b>{t}</b>\n<s><i>₴{old_price}</i></s> <b>₴{new_price}</b>\n{description1}',
                           reply_markup=markup,
                           parse_mode='HTML')
    f.close()


#------------------------------------------------------------------------------------------------------------------------------

# обробник команди /start
@bot.message_handler(commands=['start', 'goods_list'])
def start(message: str) -> None:
    """
    (message: str) - то анотація, вказуємо тип даних аргументу message
    (-> None) - тут ми вкауємо, що функція нічого не повертає
    """
    cht = message.chat.id

    with open('users.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Додаємо ідентифікатор, якщо він вже не існує у списку
    if cht not in data["chat_ids"]:
        data["chat_ids"].append(cht)

    # Зберігаємо оновлені дані у файлі
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    bot.send_message(cht, 'Вітаю! Це магазин ляляля\nОбери дію', reply_markup=start_buttons())

@bot.message_handler(commands=['answer'])
def answer(message: str) -> None:
    cht = message.chat.id

    if cht != 1001173176:
        bot.send_message(cht, 'У Вас недостатньо повноважень для застосування команди')
    else:
        msg = bot.send_message(cht, 'id:')
        bot.register_next_step_handler(msg, answer_handler)

@bot.message_handler(commands=['help'])
def goods_list(message: str) -> None:
    cht = message.chat.id

    bot.send_message(cht, 'help', reply_markup=help())

@bot.message_handler(commands=['send_discount'])
def discount(message: str) -> None:
    cht = message.chat.id

    if cht != 1001173176:
        bot.send_message(cht, 'У Вас недостатньо повноважень для застосування команди')
    else:
        msg = bot.send_message(cht, 'Товар:')
        bot.register_next_step_handler(msg, send_discount)

# з цією штукою сам до кінця не розібрався( Воно треба для обробки інлайнових кнопок
@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    cht = call.message.chat.id

    # тут ми перевіряємо, на яку кнопку тицьнув користувач
    if call.message:
        if call.data == 'women':
            women_goods(call=call)
        if call.data == 'men':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Ви обрали чоловічі товари', reply_markup=men_goods())
        elif call.data == 'bags':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Сумки:', reply_markup=bags())
        elif call.data == 'big':
            big_bags(call)
        elif call.data == 'small':
            small_bags(call)
        elif call.data == 'backpacks':
            backpack(call)
        elif call.data == 'accessories_women':
            accessories_women(call)
        elif call.data == 'help':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='help', reply_markup=help())
        elif call.data == 'jacket':
            jacket_show(call)
        elif call.data == 'pants':
            pants_show(call)
        elif call.data == 'accessories_men':
            accessories_men(call)
         

        elif call.data == 'back_btn_men':
            bot.send_message(cht, 'Ви обрали чоловічі товари', reply_markup=men_goods())
        elif call.data == 'home_btn_men':
            bot.send_message(cht, 'Вітаю! Це магазин ляляля\nОбери дію', reply_markup=start_buttons())
        elif call.data == 'back_btn_women':
            bot.send_message(cht, 'Сумки:', reply_markup=bags())
        elif call.data == 'home_btn_women':
            bot.send_message(cht, 'Вітаю! Це магазин ляляля\nОбери дію', reply_markup=start_buttons())




        elif call.data == 'q1':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Перше питання', reply_markup=start_buttons())
        elif call.data == 'q2':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Друге питання', reply_markup=start_buttons())
        elif call.data == 'q3':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Третє питання', reply_markup=start_buttons())
        elif call.data == 'q4':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Четверте питання', reply_markup=start_buttons())
        elif call.data == 'help_specialist':
            global phone

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            phone = types.KeyboardButton('Надіслати контакт', request_contact=True)
            markup.add(phone)
            bot.send_message(cht, 'Надішли контакт', reply_markup=markup)


        # Ці блоки elif відокремлені, бо тут ціла система повернень назад :)
        elif call.data == 'back':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Вітаю! Це магазин ляляля\nОбери дію', reply_markup=start_buttons())
        elif call.data == 'back_bags':
            women_goods(call)
        elif call.data == 'home':
            bot.edit_message_text(chat_id=cht, message_id=call.message.message_id, text='Вітаю! Це магазин ляляля\nОбери дію', reply_markup=start_buttons())

# обробник тексту
@bot.message_handler(content_types=['contact'])
def text(message):
    cht = message.chat.id
    global phone

    if message.contact:
        phone = message.contact.phone_number

        keyboard = types.ReplyKeyboardRemove()
        msg = bot.send_message(cht, 'Надішли питання', reply_markup=keyboard)

        bot.register_next_step_handler(msg, q_handler)

bot.polling()