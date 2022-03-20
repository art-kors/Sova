import discord
from discord.ext import commands
import json
from pprint import pprint
import pymorphy2
import requests
import time
from spark import *
TOKEN = 'OTM3Njg4MDc3Njk3MTc5Njc4.YffYEw.IVR4EAgb_VbHp9tp24fi-dX1lWY'
bot = commands.Bot(command_prefix='!')
langs = ("ru", "en")
speaker = 'ru'
token_accu = 'gr45XT9U7BXvUyit0Hb5GSGNALK7sYiw'
token_yandex = "2f31d975-8582-4fcf-98fc-4e518de3f200"


@bot.event
async def on_ready():
    print('Ready')

@bot.command()
async def nick(ctx, member: discord.Member, nickname):
    while True:
        await member.edit(nick=nickname)


@bot.command()
async def text(ctx, *, text):
    '''переводчик, использующий языки, заданные в команде set_lang
    пример: !text Hello World!'''
    global langs
    req = f"https://api.mymemory.translated.net/get?q={text}&langpair={langs[0]}|{langs[1]}"

    sp = [req]
    res = ''
    for i in sp:
        response = requests.get(i)
        if response:
            json_response = response.json()
            res = json_response["matches"][0]["translation"]
            print(res)
    await ctx.message.channel.send(res)

@bot.command()
async def set_lang(ctx, *, text):
    '''Устанавливает языки для переводчика. По умолчанию заданы параметры ru|en
    Пример команды: !set lang ru|en'''
    global langs
    langs = tuple(text.split('|'))
    print(langs)

@bot.command()
async def help_bot(ctx):
    await ctx.message.channel.send('''!text <текст для перевода>\n!set_lang <1-ый язык>|<2-ой язык>\n!numerals согласовывает слово с числительным.\nпример: !numerals яблоко|13 \nВывод: яблок\n''')


@bot.command()
async def set_timer(ctx, *, text):
    h, m, s = list(map(int, text.split(':')))
    timer = h // 60**2 + m // 60 + s
    time.sleep(timer)
    await ctx.message.channel.send('Time X has come!')


@bot.command()
async def numerals(ctx, *, text):
    '''согласовывает слово с числительным.\n
    пример: !numerals яблоко|13 /n
    яблок'''
    morph = pymorphy2.MorphAnalyzer()
    word, num = text.split('|')
    res = morph.parse(word)[0]
    a = res.make_agree_with_number(float(num)).word
    await ctx.message.channel.send(a)

@bot.command()
async def is_alive(ctx, *, text):
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(text.strip())[0]
    res = ''
    if 'NOUN' in p.tag and 'anim' in p.tag:
        if p.tag.number == 'sing':
            if p.tag.gender == 'femn':
                res = 'Живая'
            elif p.tag.gender == 'masc':
                res = 'Живой'
            else:
                res = 'Живое'
        else:
            res = 'Живые'
    elif p.tag.animacy != 'anim' and p.tag.POS == 'NOUN':
        if p.tag.number == 'sing':
            if p.tag.gender == 'femn':
                res = 'Не живая'
            elif p.tag.gender == 'masc':
                res = 'Не живой'
            else:
                res = 'Не живое'
        else:
            res = 'Не живые'
    else:
        res = 'Не существительное'
    await ctx.message.channel.send(res)

@bot.command()
async def in_start_form(ctx, *, text):
    morph = pymorphy2.MorphAnalyzer()
    res = morph.parse(text)[0].normal_form
    await ctx.message.channel.send(res)


@bot.command()
async def analyz(ctx, *, text):
    morph = pymorphy2.MorphAnalyzer()
    res = morph.parse(text)[0]
    print(type(res.tag))
    for _ in res.tag:
        pass
    # await ctx.message.channel.send(res.tag)


@bot.command()
async def in_custom_form(ctx, *, text):
    morph = pymorphy2.MorphAnalyzer()
    word, case, num = text.split()
    res = morph.parse(word)[0].inflect({case, num})
    await ctx.message.channel.send(res[0])


@bot.command()
async def send_cat(ctx):
    req = f"https://api.thecatapi.com/v1/images/search"

    sp = [req]
    res = ''
    for i in sp:
        response = requests.get(i)
        if response:
            json_response = response.json()
            res = json_response[0]['url']
            print(res)
    await ctx.message.channel.send(res)

@bot.command()
async def weather(ctx, text):
    global token_yandex
    city, limit = text.split('|')
    longitude, latitude = find_coord(city)
    url_yandex = f"https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&[lang=ru_RU]&limit={limit}&hours=false"
    yandex_req = requests.get(url_yandex, headers={'X-Yandex-API-Key': token_yandex}, verify=False)
    yandex_json = json.loads(yandex_req.text)
    if not yandex_json:
        await ctx.message.channel.send('Ошибка')
    pprint(yandex_json)
    weather = yandex_json['forecasts']
    for i in weather:
        await ctx.message.channel.send(i['date'])

        await ctx.message.channel.send(f'condition: {i["parts"]["day"]["condition"]}')
        await ctx.message.channel.send(f'Средняя температура: {i["parts"]["day"]["temp_avg"]}')
        await ctx.message.channel.send(f'Ощущается как {i["parts"]["day"]["feels_like"]}')
        await ctx.message.channel.send(f'Направление ветра: {i["parts"]["day"]["wind_dir"]}')
        await ctx.message.channel.send(f'Скорость ветра: {i["parts"]["day"]["wind_speed"]}')

def find_coord(city):
    import requests
    coord = ()
    # Готовим запрос.
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={city}&format=json"

    # Выполняем запрос.
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        coord = toponym["Point"]["pos"]
        print(coord)
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
    coord = coord.split()
    return coord

@bot.command()
async def see_also(ctx):
    await ctx.message.channel.send('game: https://disk.yandex.ru/d/AYD2sRX7oIGpGg')
    await ctx.message.channel.send('text editor: https://disk.yandex.ru/d/8NRnNIByyjE29yg')


@bot.command()
async def meme(ctx):
    req = f"https://meme-api.herokuapp.com/gimme/1"

    sp = [req]
    res = 'Some shit'
    for i in sp:
        response = requests.get(i)
        if response:
            json_response = response.json()
            pprint(json_response)
            res = json_response['memes'][0]['preview'][-1]
            print(res)
    await ctx.message.channel.send(res)


@bot.command()
async def skyline(ctx):
    req = f"https://meme-api.herokuapp.com/gimme/r34"

    sp = [req]
    res = 'Some shit'
    for i in sp:
        response = requests.get(i)
        if response:
            json_response = response.json()
            pprint(json_response)
            res = json_response['preview'][-1]
            print(res)
    await ctx.message.channel.send(res)


@bot.command()
async def rule34(ctx):
    req = f"https://meme-api.herokuapp.com/gimme/rule34/50"

    sp = [req]
    a = set()
    res = 'Some shit'
    for i in sp:
        response = requests.get(i)
        if response:
            json_response = response.json()
            pprint(json_response)
            for i in json_response['memes']:
                res = i['url']
                a.add(res)
                with open('DB.txt', 'w+') as f:
                    f.write(res + '\n')
    with open('DB.txt', 'w+') as f:
        for i in a:
            f.write(i + '\n')
    for i in a:
        await ctx.message.channel.send(i)

@bot.command()
async def etm(ctx, *, text):
    res = encode_to_morse(text)
    await ctx.message.channel.send(res)


@bot.command()
async def mte(ctx, *, text):
    res = decode_to_morse(text)
    await ctx.message.channel.send(res)


@bot.command()
async def rtm(ctx, *, text):
    res = rus_to_morze(text)
    await ctx.message.channel.send(res)

@bot.command()
async def mtr(ctx, *, text):
    res = morze_to_rus(text)
    await ctx.message.channel.send(res)


@bot.command()
async def set_speaker(ctx, a):
    global speaker
    speaker = a


@bot.command()
async def say(ctx, *, a):
    global speaker
    try:
        obj = gTTS(text=a, lang=speaker, slow=False)
    except Exception:
        await ctx.message.channel.send('Не удается озвучить текст')
    else:
        obj.save("test.mp3")
        await ctx.message.channel.send(file=discord.File(r'E:\Python projects\DISCORD(SOVA) PROJECT\test.mp3'))
        os.remove('test.mp3')


@bot.command()
async def j_name(ctx, *, text):
    res = japan_name(text)
    await ctx.message.channel.send(res)


@bot.command()
async def helper(ctx):
    await ctx.message.channel.send('')



bot.run(TOKEN)


import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Ready"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
