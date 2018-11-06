import os
import glob
import time


class DS18B20:

    __device_file = ""

    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.__device_file = device_folder + '/w1_slave'

    def _read_temp_raw(self):
        f = open(self.__device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def get_temp(self):
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def get_ui_temp(self):
        return "%.1f" % self.get_temp()

