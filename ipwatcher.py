import requests
import json
import thread
import time

FILENAME = "myip"


def watch_ip(notify):
    ip = ""
    with open(FILENAME, "rb") as f:
        ip = f.read()
    while True:
        try:
            r = requests.get("https://api.ipify.org?format=json")
            n_ip = json.loads(r.text)["ip"]
            print("obtained", n_ip)
            if n_ip != ip:
                ip = n_ip
                with open(FILENAME, "wb") as f:
                    f.write(ip)
                notify(ip)
            time.sleep(60)
        except Exception as e:
            print("IP Watcher:", e)


def run(notify):
    thread.start_new_thread(watch_ip, (notify,))
