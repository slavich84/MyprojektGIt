import requests
import time
from bs4 import BeautifulSoup

g_url_to_parse = 'https://www.olx.ua/elektronika/'

# 'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/kvartira/gorishnyye%20plavni/?search%5Bfilter_float_price%3Afrom%5D=100000&search%5Bfilter_float_price%3Ato%5D=1000000&search%5Bfilter_float_floor%3Afrom%5D=2&search%5Bfilter_float_floor%3Ato%5D=4&search%5Bfilter_float_total_area%3Afrom%5D=50&search%5Bfilter_float_total_area%3Ato%5D=60&search%5Bfilter_float_kitchen_area%3Afrom%5D=5&search%5Bfilter_float_kitchen_area%3Ato%5D=15&search%5Bfilter_float_number_of_rooms%3Afrom%5D=2&search%5Bfilter_float_number_of_rooms%3Ato%5D=4&search%5Bphotos%5D=1'

# 'https://www.olx.ua/elektronika/'


class OlxPost:
    def __init__(self, title, href, price):
        self.title = title
        self.href = href
        self.price = price

    def __eq__(self, other):

        if isinstance(other, OlxPost):
            return self.title == other.title \
                and self.price == other.price
        return NotImplemented


    def __str__(self):
        return '{}\n{}\n{}'.format(self.title, self.href, self.price)


def tg_send_text(bot_message):
    bot_token = 'BOT FATHER TOKEN'
    chat_id = 'ВАШ ЧАТ ID'
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    requests.get(send_text)


def get__last_post():
    url = g_url_to_parse

    r = requests.get(url)
    bs = BeautifulSoup(r.text, 'html.parser')
    offers_tags = bs.find_all(class_='offer-wrapper')

    return OlxPost(offers_tags[5].strong.text,
                   offers_tags[5].find(class_='price').text.strip(),
                   offers_tags[5].a.get('href'))


prev_post = get__last_post()
while True:
    last_post = get__last_post()
    if prev_post != last_post:
        prev_post = last_post
        tg_send_text(str(last_post))
        print('send...')
    time.sleep(15)
    print('check...')
