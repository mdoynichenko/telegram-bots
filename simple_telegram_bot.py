import telebot
import requests
from datetime import datetime
import vk
import random
import json

my_token = '569ccb4de2b9d59b78da5f552b0413a6491814525ab092f438af270d37f04116df3b7e7b8836fd4114559'
v = '5.95'

session = vk.AuthSession(access_token=my_token)
vk_api = vk.API(session, v=v)

appid = '05da39de897e73b9b52ba212142d51bf'
city = 'Ryazan, RU'
city_id = 500096
time_shift = 10800

thunderstorm = u'\U0001F4A8'  # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'  # Code: 300's
rain = u'\U00002614'  # Code: 500's
snowflake = u'\U00002744'  # Code: 600's snowflake
snowman = u'\U000026C4'  # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'  # Code: 700's foogy
clearSky = u'\U00002600'  # Code: 800 clear sky
fewClouds = u'\U000026C5'  # Code: 801 sun behind clouds
clouds = u'\U00002601'  # Code: 802-803-804 clouds general
hot = u'\U0001F525'  # Code: 904
defaultEmoji = u'\U0001F300'  # default emojis


class BotUser:

    def __init__(self, id):
        self._id = id
        self._state = 5
        self._city = ''


users_dict = dict()

bot = telebot.TeleBot('1897392094:AAE8rb4WQ0KEPsHikmu647OKvFIVJA2rTkY')


@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    try:

        str_res = "Привет, " + message.from_user.first_name + "! Я МаДоБот! Приятно познакомиться!\n\n"
        str_res = str_res + "Я пока совсем маленький и мало чего умею, могу разве что погоду в Рязани подсказать, анекдот рассказать да песика показать!"
        str_res = str_res + "\n\n/weather - если интересует погода\n"
        str_res = str_res + "/joke - если интересует анекдот\n"
        str_res = str_res + "/dog - если интересует песик"
        bot.send_message(message.chat.id, str_res)
        print("/help or /start used by " + message.from_user.first_name)
        '''
        user_id = message.from_user.id
        print(user_id)
        photo_list = bot.get_user_profile_photos(user_id=user_id)
        print(photo_list.total_count)
        '''
    except Exception as e:
        print('Exception (find in /start or /help):', e)
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз')
        pass


@bot.message_handler(commands=['goat'])
def goat_command(message):
    try:
        bot.send_photo(message.chat.id, 'http://placegoat.com/500/500')
        print("/goat used by " + message.from_user.first_name)
    except Exception as e:
        print('Exception (find in /goat):', e)
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз')
        pass


@bot.message_handler(commands=['dice'])
def goat_command(message):
    num = random.randint(1, 6)
    bot.send_message(message.chat.id, "Вы бросили " + u'\U0001F3B2' + ' кубик и выпало ' + str(num))
    print("/dice used by " + message.from_user.first_name)


@bot.message_handler(commands=['dog'])
def puppy_command(message):
    try:
        num = random.randint(1, 10000)
        post = vk_api.wall.get(owner_id=-142142878, offset=num, count=1)
        print(post)
        list_url = post['items'][0]['attachments'][0]['photo']['sizes']
        max_h = 0
        max_item = 0
        for item in list_url:
            if item['height'] > max_h:
                max_h = item['height']
                max_item = item
        adr = max_item['url']
        print(adr)
        bot.send_photo(message.chat.id, adr)
        print("/dog used by " + message.from_user.first_name)
    except Exception as e:
        print("Exception (find in /dog):", e)
        bot.send_message(message.chat.id, "Не удалось получить фото песика, попробуйте еще раз")
        pass


@bot.message_handler(commands=['dad_joke'])
def djoke_command(message):
    headers = {
        'Accept': 'text/plain',
    }
    res = requests.post('https://icanhazdadjoke.com/', headers=headers)
    # data = res.json()
    print(res.content)


@bot.message_handler(commands=['insult'])
def insult_command(message):
    try:
        res = requests.get('https://evilinsult.com/generate_insult.php', params={'lang': 'ru', 'type': 'json'})
        data = res.json()
        bot.send_message(message.chat.id, data['insult'])
        print("/insult used by " + message.from_user.first_name)
    except Exception as e:
        print("Exception (find in /insult):", e)
        bot.send_message(message.chat.id, "Не удалось получить оскорбление, попробуйте еще раз")
        pass


@bot.message_handler(commands=['joke'])
def joke_command(message):
    try:
        res = requests.get('http://rzhunemogu.ru/RandJSON.aspx?CType=1')
        data = res.json(strict=False)
        strii = data['content']
        print(strii)
        bot.send_message(message.chat.id, strii)
        print("/joke used by " + message.from_user.first_name)
    except Exception as e:
        print("Exception (find in /joke):", e)
        bot.send_message(message.chat.id, "Не удалось получить анекдот, попробуйте еще раз")
        pass


@bot.message_handler(commands=['weather'])
def weather_command(message):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()

        str_sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + time_shift).strftime('%H:%M')
        str_sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + time_shift).strftime('%H:%M')
        emoji = getEmoji(data['weather'][0]['id'])

        str_res = 'ПОГОДА' + ' \n\n'
        str_res = str_res + emoji + "Сейчас в Рязани " + data['weather'][0]['description']
        str_res = str_res + '\n'
        str_res = str_res + u'\U0001F321' + "Температура: " + str(int(data['main']['temp'])) + "°C"
        str_res = str_res + " (ощущается как " + str(int(data['main']['feels_like'])) + "°C)\n"
        str_res = str_res + wind_dir_arrow(data['wind']['deg']) + "Ветер: " + str(
            data['wind']['speed']) + " м/с (" + wind_dir(data['wind']['deg']) + ")\n"
        str_res = str_res + u'\U0001F4A7' + 'Влажность: ' + str(data['main']['humidity']) + '%\n'
        str_res = str_res + u'\U0001F915' + 'Давление: ' + str(
            int(data['main']['pressure'] * 100 / 133)) + ' мм рт. ст.\n'
        str_res = str_res + "\n\nНе забудь понаблюдать за красивыми летними закатами и рассветами!\n\n"
        str_res = str_res + u'\U0001F304' + "Рассвет: " + str_sunrise + '\n'
        str_res = str_res + u'\U0001F307' + "Закат: " + str_sunset + '\n'
        bot.send_message(message.chat.id, str_res)
        print("/weather used by " + message.from_user.first_name)
        print(data['weather'][0]['id'])
    except Exception as e:
        print("Exception (find in /weather):", e)
        bot.send_message(message.chat.id, "Не удалось получить погоду, попробуйте еще раз")
        pass

@bot.message_handler(commands=['my_city'])
def my_city(message):
    try:
        if message.chat.id in users_dict:
            str_res = "Привет, я тебя знаю, твой статус был" + str(users_dict[message.chat.id]._state)
            bot.send_message(message.chat.id, str_res)
            print("cmd used by " + message.from_user.first_name)
            users_dict[message.chat.id]._state += 1
        else:
            str_res = "Привет, давай знакомиться!"
            bot.send_message(message.chat.id, str_res)
            print("cmd used by " + message.from_user.first_name)
            users_dict.update({message.chat.id:BotUser(message.chat.id)})


    except Exception as e:
        print('Exception (find in /start or /help):', e)
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз')
        pass


@bot.message_handler()
def allcmd(message):
    try:
        if message.chat.id in users_dict:
            str_res = "Привет, я тебя знаю, твой статус был" + str(users_dict[message.chat.id]._state)
            bot.send_message(message.chat.id, str_res)
            bot.send_message(message.chat.id, message.text)
            print("cmd used by " + message.from_user.first_name)
            users_dict[message.chat.id]._state += 1
        else:
            str_res = "Привет, давай знакомиться!"
            bot.send_message(message.chat.id, str_res)
            print("cmd used by " + message.from_user.first_name)
            users_dict.update({message.chat.id:BotUser(message.chat.id)})

    except Exception as e:
        print('Exception (find in /start or /help):', e)
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз')
        pass


def wind_dir(angle):
    min_d = 360
    min_id = 0
    text = 'None'
    for i in range(9):
        if abs(angle - i * 45) < min_d:
            min_d = abs(angle - i * 45)
            min_id = i
    if min_id == 8:
        min_id = 0
    if min_id == 0:
        text = "З"
    if min_id == 1:
        text = "ЮЗ"
    if min_id == 2:
        text = "Ю"
    if min_id == 3:
        text = "ЮВ"
    if min_id == 4:
        text = "В"
    if min_id == 5:
        text = "СВ"
    if min_id == 6:
        text = "С"
    if min_id == 7:
        text = "СЗ"
    return text


def wind_dir_arrow(angle):
    min_d = 360
    min_id = 0
    text = 'None'
    for i in range(9):
        if abs(angle - i * 45) < min_d:
            min_d = abs(angle - i * 45)
            min_id = i
    if min_id == 8:
        min_id = 0
    if min_id == 0:
        return u'\U000027A1'
    if min_id == 1:
        return u'\U00002197'
    if min_id == 2:
        return u'\U00002B06'
    if min_id == 3:
        return u'\U00002923'
    if min_id == 4:
        return u'\U00002B05'
    if min_id == 5:
        return u'\U00002199'
    if min_id == 6:
        return u'\U00002B07'
    if min_id == 7:
        return u'\U00002198'
    return text


def getEmoji(weatherID):
    if weatherID:
        if str(weatherID)[0] == '2' or weatherID == 900 or weatherID == 901 or weatherID == 902 or weatherID == 905:
            return thunderstorm
        elif str(weatherID)[0] == '3':
            return drizzle
        elif str(weatherID)[0] == '5':
            return rain
        elif str(weatherID)[0] == '6' or weatherID == 903 or weatherID == 906:
            return snowflake + ' ' + snowman
        elif str(weatherID)[0] == '7':
            return atmosphere
        elif weatherID == 800:
            return clearSky
        elif weatherID == 801:
            return fewClouds
        elif weatherID == 802 or weatherID == 803 or weatherID == 804:
            return clouds
        elif weatherID == 904:
            return hot
        else:
            return defaultEmoji  # Default emoji

    else:
        return defaultEmoji  # Default emoji


bot.polling()
