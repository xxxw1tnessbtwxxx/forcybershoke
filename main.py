import random
from select import select
from unicodedata import decimal
import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle


import datetime
import asyncio
import sys
import time

import sqlite3
from translate import Translator
from bot_settings import bot_settings

bot = commands.Bot(command_prefix=bot_settings['PREFIX'], intents = disnake.Intents.all(), activity = disnake.Game('developming', status = disnake.Status.online))
bot.remove_command('help')

############################################################################################################################

#####################################
# СПИСОК ID РОЛЕЙ, ГИЛД, БОТ НЕЙМ
#####################################
dev_perms = [1000009933875593366, 1000417061928960110]
high_perms = [1000009933875593366, 1000417061928960110, 1000441438431088640]
admin_perms = [1000009933875593366, 1000417061928960110, 1000441438431088640, 1000009913155719258]
support = [1000009933875593366, 1000441438431088640, 1000009913155719258, 1002486676913922058, 1000011043197702185]
mod_perms = [1000009933875593366, 1000417061928960110, 1000441438431088640, 1000009913155719258, 1000011043197702185]
db_access = [1000417061928960110]


bot_name = 'My Bot'
guild = [1000009791961309194]

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

#####################################
# BIND ОТВЕТЫ
#####################################

bot_slash_commands = (
    f'Все slash команды (вызываются через /)\n\
    **/help** - вызывает меню помощи.\n\
    **/myinfo** - вызывает информацию о вас.\n\
    **/translator** (текст) - переводит текст с английского на русский.\n\
    **/embrace** (пользователь) - обнять пользователя.n\n\
    **/kiss** (пользователь) - поцеловать пользователя.\n\
    **/slap** (пользователь) - шлепнуть пользователя.\n\
    **/beat** (пользователь) - ударить пользователяn\n\
    **/myinfo** - вызывает информацию о вашем профиле.\n\
    **/avatar** (пользователь) - отправляет вам аватарку упомянутого пользователя.\n\
    **/math** (первое число) (оператор) (второе число) - простой банальный калькулятор для действия с двумя числами.\n\n')


bot_message_commands = (
    f"Все message команды (вызываются через префикс)\n\
    **ping** - проверить на работоспособность.\n\n")

#####################################
# ДЛЯ ЭМБЕДА
#####################################

serverthumbnail = 'https://leganerd.com/wp-content/uploads/2021/01/discord-999x604.jpg'
botversion = '... version: 1.0'
serverauthor = 'server name'


############################################################################################################################

@bot.event
async def on_ready():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    print(f'Moderation bot is connected by: {st}')
    print('---------')

    with sqlite3.connect('glory.db') as db:
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS members (
            name text,
            id INTEGER,
            on_join TEXT,
            messages INTEGER,
            last_update INTEGER,
            mutetime INTEGER,
            temprole TEXT,
            tempRoleTime INTEGER
    )""")
        db.commit()
    db.close()


# ###############################################################################################################################################

# @bot.command()
# async def rainbow(inter):
#     rainbowcolors = [disnake.Color.green(), disnake.Color.red(), disnake.Color.orange(), disnake.Color.brand_red()]
#     for role in inter.author.roles:
#         if role.id in dev_perms:
#             rainbowid = 1000024220086046741
#             await role.edit(color=random.choise(rainbowcolors))
#             await asyncio.sleep(1)

# @bot.command()
# async def no_rainbow(inter):
#     for role in inter.author.roles:
#         if role.id in dev_perms:
#             await inter.remove_roles(rainbow)
#             break

# ###############################################################################################################################################


@bot.command()
async def presence_help(inter):
    for role in inter.author.roles:
        if role.id in admin_perms:
            await inter.send(f'{inter.author.mention}, вы успешно вызвали помощь по активностям:\n\
`listen` - устанавливает статус "слушает".\n\
`game` - устанавливает статус "играет".\n\
`watch` - устанавливает статус "смотрит".\n\
`competing` - устанавливает статус "соревнуется в".')
            break

@bot.slash_command(description='listen (слушает), watch (смотрит), game (играет в), competing (соревнуется в)')
async def change_presence(inter, presence, doing):
    for role in inter.author.roles:
        if role.id in admin_perms:
            values = ['listen', 'watch', 'game', 'competing']
            adminname = inter.author.nick if (inter.author.nick) else inter.author.name
            if presence == "listen":
                presencelog = bot.get_channel(1000047444362543164)
                await presencelog.send(f'{inter.author.mention} сменил мою активность на {presence} с аргументом {doing}')
                activity = disnake.Activity(type=disnake.ActivityType.listening, name = doing)
                await bot.change_presence(activity=activity)
                listenembed = disnake.Embed (
                    title=f'Вот это звук! Я надел наушники и...',
                    description=f'... теперь я слушаю `{doing}`, ну спасибо, {inter.author.mention}...',
                    colour=disnake.Color.from_rgb(240, 128, 128)
                )
                listenembed.set_thumbnail(url=serverthumbnail)
                listenembed.set_image(url='https://i.pinimg.com/originals/3d/2e/3e/3d2e3e5a266f05becb4fb522a962f105.jpg')
                await inter.send(embed=listenembed)
                return
            elif presence == "watch":
                presencelog = bot.get_channel(1000047444362543164)
                await presencelog.send(f'{inter.author.mention} сменил мою активность на {presence} с аргументом {doing}')
                activity = disnake.Activity(type=disnake.ActivityType.watching, name = doing)
                await bot.change_presence(activity=activity)
                watchembed = disnake.Embed (
                    title=f'3D очки уже на мне!',
                    description=f'В крутых очках я теперь смотрю `{doing}`, спасибо {inter.author.mention} за крутой видеоматериал!',
                    colour=disnake.Color.from_rgb(255, 20, 147)
                )
                watchembed.set_thumbnail(url=serverthumbnail)
                watchembed.set_image(url='https://avatars.mds.yandex.net/get-zen_doc/4055632/pub_601e576d86f4e22208ad7bd7_601e5cd553bb652e6a060e71/scale_1200')
                await inter.send(embed=watchembed)
                return
            elif presence == "game":
                presencelog = bot.get_channel(1000047444362543164)
                await presencelog.send(f'{inter.author.mention} сменил мою активность на {presence} с аргументом {doing}')
                activity = disnake.Activity(type=disnake.ActivityType.playing, name = doing)
                await bot.change_presence(activity=activity)
                gameembed = disnake.Embed (
                    title=f'Геймпад в руки... и... ПОГНАЛИ!',
                    description=f'Я запустил игру и теперь я играю в `{doing}`! Кстати, {inter.author.mention}, геймпад крутой!',
                    colour=disnake.Color.from_rgb(255, 20, 147)
                )
                gameembed.set_thumbnail(url=serverthumbnail)
                gameembed.set_image(url='https://avatars.mds.yandex.net/i?id=f43acd35e117442361f400890bed2e1b-5257701-images-thumbs&n=13')
                await inter.send(embed=gameembed)
                return
            elif presence == "competing":
                presencelog = bot.get_channel(1000047444362543164)
                await presencelog.send(f'{inter.author.mention} сменил мою активность на {presence} с аргументом {doing}')
                activity = disnake.Activity(type=disnake.ActivityType.competing, name = doing)
                await bot.change_presence(activity=activity)
                competingembed = disnake.Embed (
                    title=f'Спортивная форма, перчатки и на соревнование!',
                    description=f'{inter.author.mention} отправил меня соревноватся в `{doing}`. Даже не сомневайтесь, я выйграю!',
                    colour=disnake.Color.from_rgb(255, 20, 147)
                )
                competingembed.set_thumbnail(url=serverthumbnail)
                competingembed.set_image(url='http://4.bp.blogspot.com/-LSboRP4Jj5g/VpevRn5SCqI/AAAAAAAAA3Y/YKV3ULPzqLI/s1600/Baka+to+Test+to+Shoukanjuu+Ni!+full+episode+gatefull.me.png')
                await inter.send(embed=competingembed)
                return
            elif presence not in values:
                await inter.send(f'{inter.author.mention}, вы указали несуществующую активность.')
                return
    else:
        await inter.send(f'{inter.author.mention}, к сожалению у вас недостаточно прав на изменение моей активности.')
        return


@bot.event
async def on_member_join(user):
    channel = bot.get_channel(1000009793349619805)
    joinembed = disnake.Embed (
        title = f"У нас пополнение! Приветствуем {user.name}",
        description = f"Привет, {user.name}. Добро пожаловать на сервер '...', здесь тебя ждет:\n\
            1. Уютная атмосфера.\n\
            2. Активная, адекватная и честная администрация!\n\
            3. Развлечения, **собственный бот** и приятное комьюнити!",
        color = disnake.Colour.from_rgb(255, 0, 255)
    )
    joinembed.set_thumbnail(url=serverthumbnail)
    joinembed.set_footer(text=botversion)
    await channel.send(embed=joinembed)
    with sqlite3.connect('glory.db') as db:
        c = db.cursor()
        joincheck = c.execute(f"SELECT id FROM members WHERE id = '{user.id}'").fetchone()
        db.commit()
        if joincheck:
            c.execute(f"UPDATE members SET name = '{user.name}', id = '{user.id}', on_join = on_join, messages = messages, last_update = '{st}', mutetime = mutetime, temprole = 'None', tempRoleTime = '0' WHERE id = '{user.id}'")
            db.commit()
        elif c.execute(f"SELECT id FROM members WHERE id = '{user.id}'").fetchone() is None:
            c.execute(f"INSERT INTO members VALUES ('{user.name}', '{user.id}', '{user.joined_at}', '0', '{st}', '0', 'No Role', '0')")
            db.commit()
    db.close()
    return

@bot.slash_command()
async def members_db_select(inter, user: disnake.User):
    for role in inter.author.roles:
        if role.id in high_perms:
            with sqlite3.connect('glory.db') as db:
                c = db.cursor()
                check = c.execute(f"SELECT id FROM members WHERE id = '{user.id}'").fetchone()
                db.commit()
            if check is None:
                await inter.send(f'error: missing {user.mention} in database. use /member_db_update (user)')
                return
            else:
                nickname = c.execute(f"SELECT name FROM members WHERE id = '{user.id}'").fetchone()
                id = user.id
                on_join = user.joined_at
                messages = c.execute(f"SELECT messages FROM members WHERE id = '{user.id}'").fetchone()
                last_update = c.execute(f"SELECT last_update FROM members WHERE id = '{user.id}'").fetchone()
                mutetime = c.execute(f"SELECT last_update FROM members WHERE id = '{user.id}'").fetchone()
                temprole = c.execute(f"SELECT temprole FROM members WHERE id = '{user.id}'").fetchone()
                tempRoleTime = c.execute(f"SELECT tempRoleTime FROM members WHERE id = '{user.id}'").fetchone()
                db.commit()
            db.close()
            selectembed = disnake.Embed (
                title='...-*- path/:/coding:database?update -*-...',
                description=f'taked from database: `members`:\n\n\n\
                name: `{nickname}`\n\
                id: `{id}`\n\
                member_joined_at: `{on_join}`\n\
                messages_counter: `{messages}`\n\
                last_update = `{last_update}`\n\
                mutetime = `{mutetime}`\n\
                temprole = `{temprole}`\n\
                tempRoleTime = `{tempRoleTime}`\n\n\n\
                getting by `{st}`',
                color=disnake.Color.from_rgb(34, 98, 0)
            )
            selectembed.set_thumbnail(url=serverthumbnail)
            selectembed.set_image(url='https://phonoteka.org/uploads/posts/2021-05/1622258823_6-phonoteka_org-p-baza-dannikh-art-krasivo-6.jpg')
            await inter.send(f'Администратор {inter.author.mention} запросил информацию о {user.mention} из базы данных', embed=selectembed)
            break

@bot.slash_command()
async def members_db_update(inter, user: disnake.User):
    for role in inter.author.roles:
        if role.id in high_perms:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            channel = bot.get_channel(1000009793349619805)
            db = sqlite3.connect('glory.db')
            c = db.cursor()
            havecheck = c.execute(f"SELECT * FROM members WHERE id = '{user.id}'")
            check = havecheck.fetchone()
            if check is None:
                c.execute(f"INSERT INTO members VALUES('{user.name}', '{user.id}', '{user.joined_at}', '0', '{st}', '0', 'No Role', '0')")
                db.commit()
                db.close()
                db_insertembed = disnake.Embed (
                    title=f'...-*- path/:/coding:database?insert -*-...',
                    description=f'{user.mention} отсутствовал в базе данных, видимо я его пропустил :(\nНо ничего, я только что его занес туда!',
                    color=disnake.Colour.from_rgb(34, 98, 0)
                )
                db_insertembed.set_image(url="https://i.ytimg.com/vi/31HfP81oWDI/maxresdefault.jpg?7857057827")
                db_insertembed.set_thumbnail(url=serverthumbnail)
                await inter.send(embed=db_insertembed)
                break
            else:
                with sqlite3.connect('glory.db') as db:
                    c = db.cursor()
                    c.execute(f"UPDATE members SET name = '{user.name}', id = '{user.id}', on_join = '{user.joined_at}', messages = messages, last_update = '{st}', mutetime = mutetime, temprole = temprole, tempRoleTime = tempRoleTime WHERE id = '{user.id}'")
                    db.commit()
                db.close()
                insertembed = disnake.Embed (
                    title='...-*-  path/:/coding:database?update -*-...',
                    description=f'{user.mention} ваш профиль в `базе данных` был обновлен администратором {inter.author.mention}',
                    color=disnake.Colour.from_rgb(34, 98, 0)
                )
                insertembed.set_thumbnail(url=serverthumbnail)
                insertembed.set_image(url='https://i.ytimg.com/vi/31HfP81oWDI/maxresdefault.jpg?7857057827')
                await inter.send(embed=insertembed)
                break
    else:
        await inter.send(f'Уважаемый {inter.author.mention}, к сожалению у вас нет прав на выполнение данной команды.')

# @bot.event
# async def on_member_update(before, after):
#     logchannel = bot.get_channel(1001538600523018350)
#     updateembed = disnake.Embed (
#         title=f'Пользователь {before.nick} был обновлен.',
#         description=f'Никнейм:\nБыл: `{before.nick}`\nСтал: `{after.nick}`'
#     )
#     await logchannel.send(embed=updateembed)

# @bot.command()
# async def role_users(inter, checkrole: disnake.Role):
#     for role in inter.author.roles:
#         if role.id in mod_perms:
#             msg = checkrole.members
#             for name in msg:
#                 endname = name
#                 role_users_embed = disnake.Embed(
#                     title=f'Пользователи с ролью {role.name}',
#                     description=f'{endname}'
#                 )
#                 await inter.send(embed=role_users_embed)
#                 await inter.send(endname)
#                 break



# @bot.event
# async def on_command_error(inter, error):
#     if isinstance(error, commands.CommandOnCooldown):
#         await inter.send(f'{inter.author.mention}, на эту команду наложена перезарядка, попробуйте через {round(error.retry_after, 2)} секунд.')


@bot.slash_command(description='+ (сложить), - (вычесть), / (поделить), ** (возвести в степень), % (остаток от деления)')
async def math(inter, firstnum: float, operator, secondnum: float):
    a = firstnum
    b = secondnum
    operations = ['+', '-', '/', '**', '%']
    if operator not in operations:
        return await inter.send(f'{inter.author.mention}, Вы указали неверные действия. Ознакомьтесь с операторами в описании команды ')
    elif operator == '+':
        c = a + b
        await inter.send(f'Сумма `{a}` и `{b}` равна `{c}`.')
        return
    elif operator == '-':
        c = a - b
        await inter.send(f'Разность `{a}` от `{b}` равна `{c}`.')
        return
    elif operator == '/':
        c = a / b
        await inter.send(f'Частное `{a}` и `{b}` равно `{c}`.')
        return
    elif operator == '**':
        c = a ** b
        await inter.send(f'Результат от возведения `{a}` в степень `{b}` равен `{c}`.')
        return
    elif operator == '%':
        c = a % b
        await inter.send(f'Остаток от деления `{a}` на `{b}` равен `{c}`.')
        return
        

@bot.slash_command()
async def db_members(inter):
    for role in inter.author.roles:
        if role.id in db_access:
            with sqlite3.connect('glory.db') as db:
                c = db.cursor()
                names = c.execute("SELECT name FROM members").fetchall()
                ids = c.execute("SELECT id FROM members").fetchall()
                on_join = c.execute("SELECT on_join FROM members").fetchall()
                messages = c.execute("SELECT messages FROM members").fetchall()
                last_update = c.execute("SELECT last_update FROM members").fetchall()

                mutetime = c.execute("SELECT mutetime FROM members").fetchall()
                temprole = c.execute("SELECT temprole FROM members").fetchall()
                tempRoleTime = c.execute("SELECT tempRoleTime FROM members").fetchall()
                db_membersembed = disnake.Embed (
                    title='',
                    description=f'`Names:` {names}\n\n\
                    `ids:` {ids}\n\n\
                    `on_join:` {on_join}\n\n\
                    `messages:` {messages}\n\n\
                    `last_update:` {last_update}\n\n\
                    `mutetime:` {mutetime}\n\n\
                    `temprole:` {temprole}\n\n\
                    `tempRoleTime:` {tempRoleTime}\n\n'
                )
                await inter.send(f'Запрос БД от администратора {inter.author.mention}', embed=db_membersembed)
                break


@bot.slash_command()
async def tempmute(inter, user: disnake.Member, mutetime: int, reason = 'Причина не указана'):
    for role in inter.author.roles:
        if role.id in mod_perms:
            muterole = user.guild.get_role(1000828532324319352)
            for muted in user.roles:
                if muterole in user.roles:
                    await inter.send(f'Пользователь {user.mention} уже имеет блокировку чата.')
                    return
                elif user.top_role >= inter.author.top_role:
                    await inter.send(f'{inter.author.mention} вы не можете применять модераторские действия к участникам, у которых есть роли выше вашей.')
                    return
                elif role.id in mod_perms:
                    await user.add_roles(muterole)
                    await inter.send(f'{user.mention} получил блокировку чата по причине `{reason}` на `{mutetime}` минут.')
                    with sqlite3.connect('glory.db') as db:
                        c = db.cursor()
                        insert = c.execute(f"UPDATE members SET mutetime = {mutetime} WHERE id = '{user.id}'")
                        db.commit()
                        mutetimeFromDb = c.execute(f"SELECT mutetime FROM members WHERE id = '{user.id}'")
                        fetch = mutetimeFromDb.fetchone()
                        db.commit()
                        strfetch = fetch[0]
                        mutetimeforunmute = strfetch
                    db.close()
                    while mutetimeforunmute != 0:
                        mutetimeforunmute -= 1
                        await asyncio.sleep(60)
                    if mutetimeforunmute == 0:
                        await user.remove_roles(muterole)
                        await inter.send(f'{user.mention}, ваша блокировка чата была снята автоматически. Общайтесь вновь!')
                        with sqlite3.connect('glory.db') as db:
                            c = db.cursor()
                            c.execute(f"UPDATE members SET mutetime = 0 WHERE id = '{user.id}'")
                            db.commit()
                        db.close()
                    return

@bot.slash_command()
async def unmute(inter, user: disnake.Member, reason = 'Причина не указана'):
    for role in inter.author.roles:
        if role.id in mod_perms:
            muterole = user.guild.get_role(1000828532324319352)
            if reason == 'Причина не указана':
                logchannel = bot.get_channel(1000047355179057323)
                await user.remove_roles(muterole)
                await inter.send(f'Модератор {inter.author.mention} снял бан чата пользователю {user.mention} без причины!')
                await logchannel.send(f'{inter.author.mention} размутил без причины {user.mention} в канале {inter.channel.mention} в `{st}`. ')
                with sqlite3.connect('glory.db') as db:
                    c = db.cursor()
                    c.execute(f"UPDATE members SET mutetime = '0' WHERE id = '{user.id}'")
                    db.commit()
                db.close()
                break
            elif reason:
                logchannel = bot.get_channel(1000047355179057323)
                await user.remove_roles(muterole)
                await inter.send(f'Модератор {inter.author.mention} снял бан чата пользователю {user.mention} по причине: `{reason} в {st}. `')
                await logchannel.send(f'{inter.author.mention} размутил {user.mention} в канале {inter.channel.mention} по причине `{reason}`.')
                with sqlite3.connect('glory.db') as db:
                    c = db.cursor()
                    c.execute(f"UPDATE members SET mutetime = '0' WHERE id = '{user.id}'")
                    db.commit()
                db.close()
                break
            else:
                await inter.send(f'{inter.author.mention}, у вас недостаточно прав для данной команды.')
                



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content == 'reset':
        return
    else:
        await bot.process_commands(message)
        if len(message.content) >= 4:
            with sqlite3.connect('glory.db') as db:
                c = db.cursor()
                add = c.execute(f"UPDATE members SET messages = messages + 1 WHERE id = '{message.author.id}'")
                db.commit()
            db.close()
            return

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def reset_all_messages(inter):
    for role in inter.author.roles:
        if role.id in high_perms:
            try:
                await inter.send(f'{inter.author.mention}, подтвердите очистку всех сообщений в базе данных, написав: `reset`. (на ответ 10 секунд)')
                respone = await bot.wait_for('message', timeout=10)
            except asyncio.TimeoutError:
                await inter.send(f'{inter.author.mention}, время на подтверждение (10 секунд) вышло.')
                return
            if respone.content.lower() not in ('reset'):
                await inter.send(f'{inter.author.mention} вы отказались от подтверждения действий.')
                return
            else:
                with sqlite3.connect('glory.db') as db:
                    c = db.cursor()
                    c.execute("UPDATE members SET messages = 0")
                    db.commit()
                    await inter.send(f'{inter.author.mention} вы успешно сбросили счетчик сообщений сервера.')
                db.close()
                return

@bot.event
async def on_member_remove(user):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    logchannel = bot.get_channel(1000047279123734648)
    channel = bot.get_channel(1000009793349619805)
    with sqlite3.connect('glory.db') as db:
        c = db.cursor()
        getdbmessage = c.execute(f"SELECT messages FROM members WHERE id = '{user.id}'").fetchone()
        db.commit()
        getlastupdate = c.execute(f"SELECT last_update FROM members WHERE id = '{user.id}'").fetchone()
        db.commit()
    db.close()
    removeembed = disnake.Embed (
        title=f'К сожалению, от нас ушел один участник, и это был - **{user.name}** =(',
        description=f'Он(-а) присоединился(-ась) к нам `{user.joined_at}`\n\
Имел(-а) `{getdbmessage}` сообщений.\n\
Ее последнее обновление модератором было `{getlastupdate}`\n\n\
Пожелаем ему(-ей) удачи и ждем возвращения снова!',
        color=disnake.Colour.from_rgb(219, 112, 147)
    )
    removeembed.set_thumbnail(url=serverthumbnail)
    removeembed.set_image(url='https://i.gifer.com/L9vO.gif')
    await channel.send(embed=removeembed)
    await logchannel.send(embed=removeembed)





@bot.slash_command()
async def members_db_remove(inter, user: disnake.User, reason):
    for role in inter.author.roles:
        if role.id in db_access:
            with sqlite3.connect('glory.db') as db:
                c = db.cursor()
                c.execute(f"DELETE FROM members WHERE id = '{user.id}'")
                db.commit()
            db.close()
            removeembed = disnake.Embed (
                title='...-*-path/:/coding:database?remove-*-...',
                description=f'{inter.author.mention} удалил из базы данных {user.mention} по причине: `{reason}`.',
                color=disnake.Colour.from_rgb(34, 98, 0)
            )
            removeembed.set_thumbnail(url=serverthumbnail)
            removeembed.set_image(url='https://i.ytimg.com/vi/31HfP81oWDI/maxresdefault.jpg?7857057827')
            await inter.send(embed=removeembed)
            break
    else:
        await inter.send(f'{inter.author.mention}, у вас НЕТ прав на эту команду.')


@bot.slash_command()
async def getinfo(inter, user: disnake.Member):
    servernick = user.nick if (user.nick) else user.name
    for role in inter.author.roles:
        if role.id in mod_perms:
            with sqlite3.connect('glory.db') as db:
                c = db.cursor()
                getmessages = c.execute(f"SELECT messages FROM members WHERE id = '{inter.author.id}'").fetchone()
                db.commit()
            db.close()
            my_infoembed = disnake.Embed (
            title = f'{inter.author.name}, **информация** о пользователе {servernick} успешно загружена!',
            description = f'1. Его никнейм на сервере: **{servernick}**\n\
            2. Его никнейм в Discord: **{user.name}**\n\
            3. Его уникальный ID: **{user.id}**\n\
            4. Его количество сообщений на сервере: **{getmessages}**\n\
            4. Он присоединились на сервер: **{user.joined_at}**\n\
            5. Его наивысшая роль: **{user.top_role}**\n\
            6. Его активность сейчас: **{user.status}**\n\
            7. Его статус сейчас:   **{user.activity}**',
            color=disnake.Colour.from_rgb(238, 130, 238)
    )
    my_infoembed.set_thumbnail(url=user.avatar.url)
    my_infoembed.set_image(url='https://i.artfile.ru/2211x1236_967840_[www.ArtFile.ru].jpg')
    await inter.send(embed=my_infoembed)
            

@bot.slash_command()
async def myinfo(inter):
    servernick = inter.author.nick if (inter.author.nick) else inter.author.name
    with sqlite3.connect('glory.db') as db:
        c = db.cursor()
        getmessages = c.execute(f"SELECT messages FROM members WHERE id = '{inter.author.id}'").fetchone()
        db.commit()
    db.close()
    my_infoembed = disnake.Embed (
        title = f'{inter.author.name}, ваша **информация** успешно загружена!',
        description = f'1. Ваш никнейм на сервере: **{servernick}**\n\
            2. Ваш никнейм в Discord: **{inter.author.name}**\n\
            3. Ваш уникальный ID: **{inter.author.id}**\n\
            4. Количество сообщений на сервере: **{getmessages}**\n\
            5. Вы присоединились на сервер: **{inter.author.joined_at}**\n\
            6. Ваша наивысшая роль: **{inter.author.top_role}**\n\
            7. Ваша активность сейчас: **{inter.author.status}**\n\
            8. Ваш статус сейчас:   **{inter.author.activity}**',
            color=disnake.Colour.from_rgb(238, 130, 238)
    )
    my_infoembed.set_thumbnail(url=inter.author.avatar.url)
    my_infoembed.set_image(url='https://i.artfile.ru/2211x1236_967840_[www.ArtFile.ru].jpg')
    await inter.send(embed=my_infoembed)


@bot.slash_command(name='translator', description='Переводит заданный текст с Английского на Русский язык')
async def translate(inter, fromlang, tolang, text):
    translator = Translator(from_lang=fromlang, to_lang=tolang)
    end_text = translator.translate(text=text)
    await inter.send(f'{end_text}')

@bot.slash_command()
async def help(inter):
    usernick = inter.author.name if (inter.author.name) else inter.author.nick
    helpembed = disnake.Embed (
        title = f'**{usernick}**, вы успешно вызвали помощь по командам.',
        description = f"{bot_slash_commands} {bot_message_commands}",
        color = disnake.Colour.from_rgb(255, 20, 147)
    )
    await inter.send(embed=helpembed, delete_after=10.0)


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(inter):
    for role in inter.author.roles:
        if role.id in admin_perms:
            pingembed = disnake.Embed(
                title=f'🎾   **Pong!**',
                description=f'Работоспособность была проверена администратором {inter.author.mention}. Моя задержка сейчас: `{bot.latency}s`.'
            )
            await inter.send(embed=pingembed)
            return
    else:
        msg = (f'**Понг!**')
        await inter.send(msg)
        return

@bot.slash_command()
async def clear(inter, amount = 0):
    for role in inter.author.roles:
        if role.id in mod_perms:
            nickname = inter.author.name if (inter.author.name) else inter.author.nick

            await inter.channel.purge(limit=int(amount))

            clearembed = disnake.Embed (
                title = f'Очистка сообщений от модератора {nickname}!',
                description = f'Модератор {nickname} очистил в чате {amount} сообщений!',
                color = disnake.Colour.from_rgb(106, 192, 245)
            )
            clearembed.set_footer(text='disnake test')
            await inter.send(embed=clearembed, delete_after=5)
            break
    else:
        nickname = inter.author.name if (inter.author.name) else inter.author.nick
        await inter.send(f'Уважаемый **{inter.author.mention}**, у вас НЕТ прав на **данную** команду!')

@bot.command()
async def clear_all(inter, amount=10000):
    for role in inter.author.roles:
        if role.id in high_perms:
            nickname = inter.author.name if (inter.author.name) else inter.author.nick

            await inter.channel.purge(limit=int(amount))

            clearembed = disnake.Embed (
                title = f'Очистка сообщений от модератора {nickname}!',
                description = f'Модератор {nickname} очистил все сообщения в чате!',
                color = disnake.Colour.from_rgb(106, 192, 245)
            )
            clearembed.set_footer(text='disnake test')
            await inter.send(embed=clearembed)
            break
    else:
        nickname = inter.author.name if (inter.author.name) else inter.author.nick
        await inter.send(f'Уважаемый **{inter.author.mention}**, у вас НЕТ прав на **данную** команду!')

@bot.event
async def on_message_edit(before, after):
    editlog = bot.get_channel(1000047245170847825)
    editlogEmbed = disnake.Embed(
        title=f'Message updated by {before.author.name}', 
        description=f'{before.author.mention} отредактировал сообщение в {before.channel.mention}:\n\nБыло: {before.content}\nСтало: {after.content}'
    )
    editlogEmbed.set_footer(text=st)
    for mybot in before.author.name:
        if before.author.name != bot_name:
            await editlog.send(embed=editlogEmbed)
            return




@bot.event
async def on_message_delete(message):
    deletelog = bot.get_channel(1000047261595738243)
    deletelogEmbed = disnake.Embed(
        title = f'Message deleted by {message.author.name}',
        description = f'{message.author.name} удалил сообщение `{message.content}` из канала: {message.channel.mention}.'
    )
    deletelogEmbed.set_footer(text=st)
    for mybot in message.author.name:
        if message.author.name != bot_name:
            await deletelog.send(embed=deletelogEmbed)
            with sqlite3.connect('glory.db') as db:
                c = db.cursor()
                removeone = c.execute(f"UPDATE members SET messages = messages - 1 WHERE id = '{message.author.id}'")
                db.commit()
            db.close()
            return

@bot.slash_command()
async def kick(inter, user: disnake.User, reason = "Причина не указана"):
    for role in inter.author.roles:
        if role.id in mod_perms:
            if user.top_role >= inter.author.top_role:
                await inter.send(f'{inter.author.mention} вы не можете применять модераторские команды к пользователям, у которого есть роль выше вашей!')
                return
            for role in inter.author.roles:
                if role.id in mod_perms:
                    await user.kick(reason=reason)
                    kickembed = disnake.Embed (
                        title=f'Участник {user.name} был кикнул с сервера.',
                        description=f'Модератор {inter.author.mention} исключил с сервера участника {user.id} с причиной: `{reason}`',
                        color=disnake.Color.from_rgb(255, 222, 173)
                    )
                    kickembed.set_thumbnail(url=user.avatar.url)
                    kickembed.set_image(url='https://avatars.mds.yandex.net/i?id=bad11e4abdd060f9ea66566379ef5bf4-3948822-images-thumbs&n=13')
                    await inter.send(embed=kickembed)
                    return
    else:
        await inter.send(f'{inter.author.mention}, у вас нет прав на данную команду.')

@bot.slash_command(description='Получить аватар пользователя')
async def getavatar(inter, user: disnake.Member):
    usernick = user.nick if (user.nick) else user.name
    embed = disnake.Embed (
        title=f'',
        description=f'Аватар пользователя **{usernick}**'
    )
    embed.set_image(user.avatar)
    await inter.send(f'{user.mention}, пользователь {inter.author.mention} ворует вашу аватарку!!!')
    await inter.send(embed=embed)


@bot.slash_command(description='Поцеловать пользователя')
@commands.cooldown(1, 3, commands.BucketType.user)
async def kiss(inter, user: disnake.Member):
    authornick = inter.author.nick if (inter.author.nick) else inter.author.name
    usernick = user.nick if (user.nick) else user.name
    kissembed = disnake.Embed (
        title=f'Пользователь {authornick} поцеловал пользователя {usernick}'
    )
    kissembed.set_image(url='https://lifeo.ru/wp-content/uploads/gif-anime-kisses-35.gif')
    await inter.send(embed=kissembed)

@bot.slash_command(description='Обнять пользователя')
@commands.cooldown(1, 3, commands.BucketType.user)
async def embrace(inter, user: disnake.Member):
    authornick = inter.author.nick if (inter.author.nick) else inter.author.name
    usernick = user.nick if (user.nick) else user.name
    embraceembed = disnake.Embed (
        title=f'Пользователь {authornick} обнять пользователя {usernick}'
    )
    embraceembed.set_image(url='https://c.tenor.com/OuA7Ogvhb2cAAAAC/hugging-hug.gif')
    await inter.send(embed=embraceembed)

@bot.slash_command(description='Шлепнуть пользователя')
@commands.cooldown(1, 3, commands.BucketType.user)
async def slap(inter, user: disnake.Member):
    authornick = inter.author.nick if (inter.author.nick) else inter.author.name
    usernick = user.nick if (user.nick) else user.name
    slapembed = disnake.Embed (
        title=f'Пользователь {authornick} шлепнул пользователя {usernick}'
    )
    slapembed.set_image(url='https://c.tenor.com/XiYuU9h44-AAAAAC/anime-slap-mad.gif')
    await inter.send(embed=slapembed)

@bot.slash_command(description='Ударить пользователя')
@commands.cooldown(1, 3, commands.BucketType.user)
async def beat(inter, user: disnake.Member):
    authornick = inter.author.nick if (inter.author.nick) else inter.author.name
    usernick = user.nick if (user.nick) else user.name
    beatembed = disnake.Embed (
        title=f'Пользователь {authornick} ударил пользователя {usernick}'
    )
    beatembed.set_image(url='https://i.gifer.com/P44M.gif')
    await inter.send(embed=beatembed)

@bot.slash_command(description='Выдать временную роль (admin)')
async def temprole(inter, user: disnake.Member, roleget: disnake.Role, time: int):
    for role in inter.author.roles:
        if role.id in admin_perms:
            if time is None:
                return
            else:
                roleid = roleget.id
                botgetrole = user.guild.get_role(roleid)
                channellog = bot.get_channel(1002870162363535391)
                await inter.send(f'{inter.author.mention} выдал роль {roleget.mention} пользователю {user.mention} на {time} минут.')
                await user.add_roles(botgetrole)
                with sqlite3.connect('glory.db') as db:
                    c = db.cursor()
                    add = c.execute(f"UPDATE members SET temprole = '{roleget.name}', tempRoleTime = '{time}' WHERE id = '{user.id}'")
                    db.commit()
                db.close()
                countertime = time
                while countertime > 0:
                    countertime -= 1
                    await asyncio.sleep(60)
                    if countertime == 0:
                        await user.remove_roles(botgetrole)
                        await inter.send(f'{user.mention}, ваша роль **{roleget.mention}** была снята автоматически.')
                        with sqlite3.connect('glory.db') as db:
                            c = db.cursor()
                            insert = c.execute(f"UPDATE members SET temprole = 'None', tempRoleTime = '0' WHERE id = '{user.id}'")
                            db.commit()
                        db.close()
                        return

######################################################################### TICKETS TICKETS TICKETS TICKETS TICKETS TICKETS TICKETS TICKTES
# class Ticket(commands.Cog):

#     @bot.command()
#     async def startticket(inter):
#         guild = 1000009791961309194
#         ticketchannelid = bot.get_channel(1001549637532012665)
#         button = disnake.ui.View()
#         button.add_item(disnake.ui.Button(style=disnake.ButtonStyle.green, emoji = '📔'))
#         await ticketchannelid.send('Нажмите на кнопку для создания тикета.', view=button)

#     @bot.event
#     async def on_message_interaction(inter):
#         ticketchannelid = bot.get_channel(1001549637532012665)
#         category = disnake.utils.get(inter.guild.categories, name="активные жалобы")
#         for ch in category.channels:
#             if ch.topic == inter.author.id:
#                 await ticketchannelid.send(f'{inter.author.mention} у вас уже есть тикет, постарайтесь решить оставшийся вопрос в нем.')
#                 return
#         else:
#             support = inter.guild.get_role(1002486676913922058)
#             everyone = inter.guild.get_role(1000009791961309194)
#             overwrites = { 
#                 everyone:disnake.PermissionOverwrite(read_messages=False),
#                 inter.me:disnake.PermissionOverwrite(read_messages=True),
#                 inter.author:disnake.PermissionOverwrite(read_messages=True),
#                 support:disnake.PermissionOverwrite(read_messages=True, send_messages=True)
#             }
#             newticket = await category.create_text_channel(name=f'{inter.author.name} ticket.', overwrites=overwrites)
#             await ticketchannelid.send(f'{inter.author.mention} вы успешно создали тикет!')
#             return

#     @bot.slash_command()
#     async def close(inter, reason):
#         support = inter.guild.get_role(1002486676913922058)
#         for role in inter.author.roles:
#             if role.id in support:
#                 overwrite = disnake.PermissionsOverwrite()
#                 overwrite.send_messages = False
#                 overwrite.view_channel = False
#                 await inter.send(f'Тикет был закрыт.')
#                 await inter.channel.set_permissions(overwrite=overwrite)
#                 return


bot.run(bot_settings['TOKEN'])