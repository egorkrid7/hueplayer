# -*- coding: utf-8 -*-
import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('278758102:AAENnsnUdlaLTklqCaoj0F8hSckxoR-_t10')

@bot.message_handler(commands=['start'])
def default_test(message):
    bot.send_message(message.from_user.id, 'Please input audio track title or performer\'s name.')


@bot.message_handler(content_types=["text"])
def _query(message):
    url = 'https://downloadmusicvk.ru/audio/search?q=' + parser(message.text)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    counter = 1
    for link in soup.findAll('div', {'class' : 'row audio'}, limit=5):
        name_of_song = link.find('div', {'class' : 'col-lg-9 col-md-8 col-sm-7 col-xs-5'}).text
        # go to 3rd block
        link_to_download = link.find('div', {'class' : 'col-lg-2 col-md-3 col-sm-4 col-xs-5'})
        # go to download button
        link_to_download = link_to_download.find('a', {'class' : 'btn btn-primary btn-xs download'})

        # link to page to download
        main_link = 'https://downloadmusicvk.ru' + link_to_download.get('href')
        # link to download
        answer = handle_song(main_link)

        code = '<a href=\"' + answer + '\">' + str(counter) + '. ' + name_of_song.strip() + '</a>'
        bot.send_message(message.from_user.id, parse_mode='HTML', text = code)
        counter += 1

def handle_song(main_link):
    source_code = requests.get(main_link)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    button = soup.find('a', {'class' : 'btn btn-success btn-lg btn-block download'})
    return 'https://downloadmusicvk.ru' + button.get('href')


def parser(message):
    message = message.strip()
    answer = ""
    for c in message:
        if c != " ":
            answer += c
        else:
            answer += '+'
    return answer


if __name__ == '__main__':
     bot.polling(none_stop=True)


