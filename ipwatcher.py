import requests
import json
import threading
import time
import os
import fucking_dom_ru

FILENAME = "myip"
DELAY = 60


class IPWatcher(threading.Thread):
    cancel_flag = False
    notify = None

    def __init__(self, notify):
        threading.Thread.__init__(self)
        self.notify = notify

    def run(self):
        print("Starting " + self.name)
        self.watch_ip()
        print("Exiting " + self.name)

    def stop(self):
        self.cancel_flag = True

    def watch_ip(self):
        ip = ""
        if os.path.isfile(FILENAME):
            with open(FILENAME, "rb") as f:
                ip = f.read().decode()
        else:
            with open(FILENAME, "wb") as f:
                f.write(bytes("".encode("utf-8")))
        while not self.cancel_flag:
            try:
                n_ip = fucking_dom_ru.get_fucking_dom_ru_ip()
                print("obtained", n_ip)
                if n_ip != ip:
                    ip = n_ip
                    with open(FILENAME, "wb") as f:
                        f.write(bytes(ip.encode("utf-8")))
                    self.notify(ip)
                time.sleep(DELAY)
            except Exception as e:
                print("IP Watcher:", e)


def run(notify):
    thread = IPWatcher(notify)
    thread.start()
    return thread


def notify_test(ip):
    print("notify_test", ip)


if __name__ == "__main__":
    t = run(notify_test)
    time.sleep(2 * DELAY)
    t.stop()
