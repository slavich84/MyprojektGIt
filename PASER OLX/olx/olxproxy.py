import requests
import time
from bs4 import BeautifulSoup


g_url_to_parse = 'https://www.olx.ua/elektronika/'


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
    bot_token = 'BOTFARHER TOKEN'
    chat_id = 'ВАШ ЧАТ ID'
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    requests.get(send_text)


def get_last_post():
    url = g_url_to_parse

    proxies = {
        'http': 'http://186.211.185.106:49314',
        # 'https': 'http://186.211.185.106:49314',
    }

    # Create the session and set the proxies.
    s = requests.Session()
    s.proxies = proxies

    r = s.get(url)
    bs = BeautifulSoup(r.text, 'html.parser')
    offers_tags = bs.find_all(class_='offer-wrapper')

    return OlxPost(offers_tags[5].strong.text,
                   offers_tags[5].find(class_='price').text.strip(),
                   offers_tags[5].a.get('href'))


prev_post = get_last_post()

while True:
    last_post = get_last_post()
    if prev_post != last_post:
        prev_post = last_post
        tg_send_text(str(last_post))
        print('send...')
    time.sleep(15)
    print('check...')
