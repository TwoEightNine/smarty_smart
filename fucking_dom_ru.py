#! -*- coding: utf-8 -*-
import requests


def get_fucking_dom_ru_ip():
    r = requests.get("http://192.168.0.1/ER_tel_status.html").text
    r = r.replace('\t', '').replace('\n', '').replace(' ', '')
    r = r[r.find('<p>IP'):r.find('<p>MAC')]
    r = r[r.find('<span>') + 6:r.find('</span>')]
    return r


if __name__ == "__main__":
    print(get_fucking_dom_ru_ip())