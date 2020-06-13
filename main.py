from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command,Text
from aiogram.types import Message,ReplyKeyboardRemove
import aiohttp
import keyboards
from status import TEST
import config
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import func
import sqlite as sql
import time
import asyncio




PROXY_URL ='http://104.227.97.168:8000'


PROXY_AUTH = aiohttp.BasicAuth(login='qY5bWs', password='kjMHoV')

FIRST_POST={'title':'','url':'','price':'','img':''}

storage = MemoryStorage()
bot = Bot(token=config.API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)

#bot = Bot(token=config.API_TOKEN)

dp = Dispatcher(bot,storage=storage)

async def replace_link(link:str):
    st=link
    if link.startswith('https://m.avito.ru'):
        st=link.replace('https://m.avito.ru','https://www.avito.ru')
    elif link.startswith('http://m.avito.ru'):
        st=link.replace('http://m.avito.ru','https://www.avito.ru')
    elif link.startswith('m.avito.ru'):
        st=link.replace('m.avito.ru','https://www.avito.ru')
    elif link.startswith('www.avito.ru'):
        st=link.replace('www.avito.ru','https://www.avito.ru')
    return st


async def write_link(message: types.Message,state:FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await message.reply(config.WELCOM_TEXT, reply_markup=keyboards.main_menu)
    else:
        link_tp=str(message.text).strip()
        link=await replace_link(link_tp)

        tstap=func.check_link(link)
        if tstap!=None:

            async with state.proxy() as data:
                data['Q1'] = link
            try:
                flag=False
                if sql.select_users_check_user_time(message.chat.id):
                    if sql.update_user_link(message.chat.id,link,tstap):
                        flag=True

                else:
                    if sql.add_users_user(message.chat.id,link,0,24,tstap):
                        flag = True
                if flag==True:
                    await message.reply(config.WRITE_LINK_TEXT, reply_markup=keyboards.main_menu)
                    await state.finish()
                else:
                    await message.reply(config.BAD_ADD_LINK, reply_markup=keyboards.back_menu)
            except:
                await message.reply(config.BAD_ADD_LINK, reply_markup=keyboards.back_menu)

        else:
            print('неправильная ссылка')
            await message.reply(config.BAD_LINK_TEXT, reply_markup=keyboards.back_menu)

async def write_time(message: types.Message,state:FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await message.reply(config.WELCOM_TEXT, reply_markup=keyboards.main_menu)
    else:
        kt=func.check_time(message.text)
        if kt!=None:

            async with state.proxy() as data:
                data['Q2'] = str(message.text).strip()
                if sql.update_user_time(message.chat.id,kt[0],kt[1]):

                    await message.reply(config.WRITE_TIME_TEXT, reply_markup=keyboards.main_menu)
                    await state.finish()
                else:
                    await message.reply(config.BAD_WRITE_TIME_TEXT, reply_markup=keyboards.back_menu)

        else:
            print('неправильное время')
            await message.reply(config.BAD_WRITE_TIME_TEXT, reply_markup=keyboards.back_menu)




async  def send_welcom(message: types.Message):
    await message.reply(config.WELCOM_TEXT, reply_markup=keyboards.main_menu)

async  def send_back_welcom(message: types.Message):
    await message.reply(config.BACK_TEXT, reply_markup=keyboards.main_menu)


async  def send_help(message: types.Message):
   await message.reply(config.HELP_TEXT, reply_markup=keyboards.main_menu)


async  def send_settings(message: types.Message):
    await message.reply(config.SETTINGS_TEXT, reply_markup=keyboards.settings_menu)

async  def send_add_link(message: types.Message):
    await message.reply(config.ADD_LINK_TEXT, reply_markup=keyboards.back_menu)
    await TEST.Q1.set()

async  def send_set_time(message: types.Message):
    await message.reply(config.ADD_TIME_TEXT, reply_markup=keyboards.set_time_menu)

async  def send_set_time_2(message: types.Message,state=None):
    await message.reply(config.SET_TIME_TEXT, reply_markup=keyboards.back_menu)
    await TEST.Q2.set()






@dp.message_handler(state=TEST.Q2)
async def answer_time(message:types.Message,state:FSMContext):
    answer=message.text
    await write_time(message,state)


@dp.message_handler(state=TEST.Q1)
async def answer_link(message:types.Message,state:FSMContext):
    answer=message.text
    await  write_link(message,state)






@dp.message_handler(Command("help"),state=None)
async def send_welcome(message: types.Message):
    await send_help(message)

@dp.message_handler(Text(equals=["Назад"]))
async def send_back_text(message: types.Message):
    await send_back_welcom(message)

@dp.message_handler(Text(equals=["Помощь"]))
async def send_help_text(message: types.Message):
    await send_help(message)

@dp.message_handler(Text(equals=["Настройки"]))
async def send_settings_text(message: types.Message):
    await send_settings(message)



@dp.message_handler(Text(equals=["Добавить ссылку"]))
async def send_add_link_text(message: types.Message):
    await send_add_link(message)

@dp.message_handler(Text(equals=["Настройка времени"]))
async def send_set_time_text(message: types.Message):
    await send_set_time(message)

@dp.message_handler(Text(equals=["Установить время"]))
async def send_set_time_text_2(message: types.Message):
    await send_set_time_2(message)



@dp.message_handler(Text(equals=["Управление"]))
async def send_conntrol_menu(message: types.Message):
    try:
        res = sql.select_users_user_all(message.chat.id)
        print(res)
        if res != None:
            vk = 'Мониторин выключен'
            if res[6] == 1:
                vk = 'Мониторинг включен'
            st = vk + '\nВаши настройки:\nВремя: от ' + str(res[3]) + ' до ' + str(res[4]) + '\n' + 'Ссылка: ' + str(
                res[2]) + '\n\n'

            await message.reply(st, reply_markup=keyboards.main_menu_control)
        else:
            await send_welcom(message)
    except:
        await send_welcom(message)
    #await message.reply(config.CONTOL_MONITOR_TEXT, reply_markup=keyboards.main_menu_control)






@dp.message_handler(Text(equals=["Старт"]))
async def start_monitor(message: types.Message):
    try:
        res=sql.select_users_user_all(message.chat.id)
        if res!=None:
            vk='Мониторин выключен'
            if str(res[2])!='':
                if sql.update_vk(message.chat.id,1):
                    await message.reply(config.START_MONITOR_TEXT, reply_markup=keyboards.main_menu)


            else:
                await message.reply(config.NO_LINK_TEXT, reply_markup=keyboards.main_menu)
        else:
            await message.reply(config.NO_LINK_TEXT, reply_markup=keyboards.main_menu)

    except:
        pass




@dp.message_handler(Text(equals=["Стоп"]))
async def stop_monitor(message: types.Message):
    try:
        res = sql.select_users_user_all(message.chat.id)
        if res != None:
            vk = 'Мониторин включен'
            if str(res[2]) != '':
                if sql.update_vk(message.chat.id, 0):
                    await message.reply(config.STOP_MONITOR_TEXT, reply_markup=keyboards.main_menu)

            else:
                await message.reply(config.NO_LINK_TEXT, reply_markup=keyboards.main_menu)

    except:
        pass








@dp.message_handler(Command("start"),state=None)
async def send_welcome_text(message: types.Message):
    try:
        res=sql.select_users_user_all(message.chat.id)
        print(res)
        if res!=None:
            vk='Мониторин выключен'
            if res[6]==1:
                vk='Мониторинг включен'
            st=vk+'\nВаши настройки:\nВремя: от '+str(res[3])+' до '+str(res[4])+'\n'+'Ссылка: '+str(res[2])+'\n\n'

            await message.reply(st, reply_markup=keyboards.main_menu)
        else:
            await send_welcom(message)
    except:
        await send_welcom(message)







async def start_parser():
    global FIRST_POST
    base_last=set()

    posts=[]
    new_date=0
    x=0
    try:
        print('проверка заданий в базе')
        res = sql.select_users_for_pars()

        if res!=None:
            for mas in res:
                try:
                    print('выполняем задания')
                    link=mas[2]
                    date_last=mas[5]
                    chat_id=mas[1]
                    new_date=0

                    base_last = str(mas[7]).split(',')


                    base = func.get_link(link)
                    print('записей в базе ')
                    if base != None:
                        bb=func.soup_parsing(base,base_id_items=base_last)
                        b_items = bb[0]
                        ss_last=','.join(bb[1])
                        if b_items != None:
                            if len(b_items) > 0:
                                print('записей в b_items ')
                                for m in b_items:
                                    try:


                                        date1 = func.str_to_date(m['time'])
                                        tm = date1
                                        print('проверяем дату')
                                        if tm > date_last:
                                            if tm>new_date:
                                                new_date=tm
                                            FL = True
                                            FIRST_POST['title'] = m['title']
                                            FIRST_POST['url'] = m['url']
                                            FIRST_POST['price'] = m['price']
                                            FIRST_POST['img'] = m['img']
                                            if FIRST_POST['title'] == '' or FIRST_POST['url'] == '' or FIRST_POST[
                                                'price'] == '' or FIRST_POST['img'] == '':
                                                FL = False

                                            if FL == True:
                                                sent = '<a href="{}">{}</a> \n\nцена: {}'.format(FIRST_POST['url'],
                                                                                         FIRST_POST['title'],
                                                                                         FIRST_POST['price'])


                                                posts.append({'chat_id':chat_id,'img':FIRST_POST['img'],'post':sent})



                                    except:
                                        continue

                                pflag=False

                                if len(posts)>0:
                                    print('переходим к постингу')

                                    for cap in posts:

                                        try:
                                            time.sleep(1)
                                            chat_id=cap['chat_id']
                                            img=cap['img']
                                            post=cap['post']


                                            await bot.send_photo(chat_id,img,post,parse_mode='HTML')

                                            if pflag==False:
                                                if sql.update_last_pars(chat_id,new_date,ss_last):
                                                    pflag=True


                                        except:
                                            print('error post')
                                            continue
                                    print('выполнен постинг')
                                else:
                                    print('нет постов для постинга')

                        else:

                            print('no new obv')
                    else:
                        print('empty base')

                except:
                    print('error p')
                    continue

        else:
            print('no tasks')
            return None

    except:
        return None


async def parsing(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        await start_parser()









if __name__ == '__main__':

    dp.loop.create_task(parsing(config.TIME_PARSING))
    executor.start_polling(dp, skip_updates=True)


