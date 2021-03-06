from bs4 import BeautifulSoup as bs
from datetime import date, timedelta
import datetime as DT
import requests
from fake_useragent import UserAgent
import config

FIRST_PAGES_ID="1980-10-01 10:10:10"

FIRST_POST={'title':'','url':'','price':'','img':''}

DATE_DICT={'января':'01','февраля':'02','марта':'03','апреля':'04','мая':'05','июня':'06','июля':'07','августа':'08','сентября':'09','октября':'10','ноября':'11','декабря':'12'}

proxy='socks5://aWdrxQ:YGppgp@108.187.204.26:8000'


def replace_link(link:str):
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


def soup_parsing(base,base_id_items:set):

    base_items = []
    base_list = list(base_id_items)
    base_last=set()
    for b in base:
        item = {}
        try:

            g_link = b.find('a',class_='snippet-link')['href']
            g_title = b.find('a',class_='snippet-link')['title']
            g_price = b.find('span',class_='snippet-price').text

            g_img = b.find('img',class_='large-picture-img')['src']

            g_item_id = b['data-item-id']

            g_time = b.find('div',class_='snippet-date-info')['data-tooltip']



            item['id'] = g_item_id
            item['url'] = 'https://www.avito.ru'+g_link
            item['img'] = g_img
            item['title'] = g_title
            item['price'] = g_price
            item['time'] = g_time


            if g_item_id not in base_id_items:
                base_list.append(g_item_id)
                base_items.append(item)
            else:
                print(f'id {g_item_id} в базе уже есть')
        except:
            continue
    if len(base_items)>0:
        if len(base_list)>config.LIMIT_LAST_BASE_COUNT:
            base_list.sort(reverse=True)
            while len(base_list)>config.LIMIT_LAST_BASE_COUNT:
                del (base_list[-1])
        base_last=set(base_list)
        return [base_items,base_last]
    else:
        return None


def date_plus(day:int):
    today = date.today()
    days = timedelta(day)
    new_date = today + days
    return new_date

def check_date(end_date):
    today = date.today()
    d=DT.datetime.strptime(end_date,'%Y-%m-%d').date()
    if today<=d:

        return True
    else:
        return False


def str_to_date(t):
    global DATE_DICT
    try:
        t=t+':00'
        now = DT.datetime.now()
        year = now.year
        dt_fmt = '%d.%m.%Y %H:%M:%S'
        gt = t.split(' ')

        if gt[1] in DATE_DICT:
            s = DATE_DICT[gt[1]]
            ns = f'{gt[0]}.{s}.{year} {gt[2]}'
            d = DT.datetime.strptime(ns,dt_fmt).timestamp()
            return d

    except:
        return None




def get_link(link):
    try:
        global proxy
        ua = UserAgent()
        agent = ua.random
        headers = {
            'User-Agent': agent,
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive'
        }

        get_html= requests.get(link,
                            proxies=dict(http=proxy,
                                         https=proxy),headers=headers)

        soup=bs(get_html.text,'html.parser')
        base = soup.findAll('div', class_='snippet-horizontal')
        if len(base)>0:
            return base
        else:
            return None
    except:
        return None



def check_link_update(link):
    global FIRST_PAGES_ID
    global FIRST_POST


    FIRST_PAGES_ID = "1900-10-01 10:10:10"

    dt_fmt = '%Y-%m-%d %H:%M'
    f_date = DT.datetime.strptime(FIRST_PAGES_ID,dt_fmt)
    base_id_items = set()

    st=replace_link(link)
    print(st)

    s='https://www.avito.ru'
    if st.startswith(s):
        try:
            link=st

            base = get_link(link)
            if base != None:
                b_items = soup_parsing(base,base_id_items)[0]
                if b_items != None:
                    if len(b_items) >0:
                        for m in b_items:
                            try:
                                date1=str_to_date(m['time'])
                                if date1>f_date:
                                    f_date=date1
                                    FIRST_PAGES_ID=str(f_date)
                                    FIRST_POST['title']=m['title']
                                    FIRST_POST['url'] = m['url']
                                    FIRST_POST['price'] = m['price']
                                    FIRST_POST['img'] = m['img']

                            except:
                                continue
                        return True
                else:
                    return False
        except:
            return False
    return False








def check_link(link):

    global FIRST_POST

    FIRST_PAGES_ID = "1980-10-01 10:10:10"
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    f_date = DT.datetime.strptime(FIRST_PAGES_ID,dt_fmt).timestamp()

    base_id_items = set()

    st = replace_link(link)
    print(st)

    s = 'https://www.avito.ru'

    if link.startswith(s):
        try:
            link = st

            base = get_link(link)
            if base != None:
                b_items = soup_parsing(base,base_id_items)[0]
                if b_items != None:
                    if len(b_items) >0:
                        for m in b_items:
                            try:
                                date1=str_to_date(m['time'])
                                if date1>f_date:
                                    f_date=date1
                                    FIRST_PAGES_ID=str(f_date)
                                    FIRST_POST['title']=m['title']
                                    FIRST_POST['url'] = m['url']
                                    FIRST_POST['price'] = m['price']
                                    FIRST_POST['img'] = m['img']

                            except:
                                continue
                        return f_date
                else:
                    return None
        except:
            return None
    return None

def check_time(time_data:str):
    try:
        m=time_data.split('-')
        x=int(m[0])
        y=int(m[1])
        if x>-1 and x<25 and y>-1 and y<25 and x<y:
            return (x,y)
        else:
            return None
    except:
        return None

