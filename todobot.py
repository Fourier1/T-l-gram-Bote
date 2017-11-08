#! /usr/bin/env python3.5
# -*- coding:utf-8 -*-

import json
import requests
import time
import urllib

TOKEN = "384778830:AAETOFbFM-mONaGw5kJGuoCzL7AV60mFXmw"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    """
    Télecharger l'url 
    :param str url: l'url
    :return: content
    :rtype str
    """
    response = requests.get(url)
    content = response.content.decode("utf8")
    print(content)
    return content


def get_json_from_url(url):
    """
    Convertir le resultat de l'url en json afin de pourvoir l'exploiter plus facilement
    :param srt url: l'url
    :return: js
    :rtype json
    """
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    """
    long intéruption : timeout= 100
    Récuperation des messages sur Télégram
    :param int offset: Spécifier que nous ne voulons pas tous les 
    messages reccent mais que le message qui vien juste d'arriver  
    :return: js
    :rtype json
    """
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    print(js)
    return js


def get_last_chat_id_and_text(updates):
    """
    Récuperer le message et id du message 
    :param updates: 
    :return: 
    """
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def send_message(text, chat_id):
    """
    Envoie de message a notre bot avec deux parametre necessaire 
    :param str text: lle message
    :param int chat_id: l'id du message 
    :return: 
    """
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def get_last_update_id(updates):
    """
    Récuperer les plus grand des ID de tous les messages reçus update_ids
    :return: 
    """
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    """
    envoyer echo a tous les autres message 
    :param dict updates: le messge 
    :return: 
    """
    for update in updates["result"]:
        try:
            text = update["result"]["text"]
            chat = update["result"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


def main():
    """
    executer le code en boucle et retourner a chaque demi seconde les derniers messsages  
    :return: 
    """
    last_update_id = None
    while True:
        print("Opténir des mises ajour ...")
        print()
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            print("UPDATES ID  + 1 ", last_update_id)
            echo_all(updates)
            time.sleep(0.5)


if __name__ == '__main__':
    main()
