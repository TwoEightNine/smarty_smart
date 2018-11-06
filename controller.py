from gpiozero import DigitalOutputDevice, RGBLED
import threading
import utils
import ds18b20

PIN_TEAPOT = 6
PIN_LIGHT = 14
PIN_RGB = 18
PIN_AMP = 23
PIN_LED_R = 13
PIN_LED_G = 7
PIN_LED_B = 15


class Controller:

    __teapot = None
    __light = None
    __rgb = None
    __amp = None
    __temp_teapot = None
    __temp_air = None
    __led = None

    def __init__(self):
        self.__teapot = DigitalOutputDevice(PIN_TEAPOT, active_high=False)
        self.__light = DigitalOutputDevice(PIN_LIGHT, active_high=False)
        self.__rgb = DigitalOutputDevice(PIN_RGB, active_high=False)
        self.__amp = DigitalOutputDevice(PIN_AMP, active_high=False)
        # self.__temp_teapot = ds18b20.DS18B20()
        self.__temp_air = ds18b20.DS18B20()
        self.__led = RGBLED(PIN_LED_R, PIN_LED_G, PIN_LED_B)

    def get_air_temp(self):
        return self.__temp_air.get_temp()

    def get_water_temp(self):
        return 70.1  # self.__temp_teapot.get_temp()

    def get_water_fullness(self):
        return 80

    def is_teapot_on(self):
        return self.__teapot.value

    def is_light_on(self):
        return self.__light.value

    def is_rgb_on(self):
        return self.__rgb.value

    def is_amp_on(self):
        return self.__amp.value

    def set_led(self, color):
        self.__led.color = (
            int(color[:2], 16) / 255.0,
            int(color[2:4], 16) / 255.0,
            int(color[4:], 16) / 255.0
        )

    def get_led_color(self):
        color = self.__led.value
        return hex(int(color[0] * 255))[2:] \
               + hex(int(color[1] * 255))[2:] \
               + hex(int(color[2] * 255))[2:]

    def turn_on_teapot(self, on_boil):
        self.__teapot.on()
        threading.Thread(target=self.__wait_until_boil, args=(on_boil,)).start()

    def toggle_light(self):
        self.__light.toggle()

    def toggle_rgb(self):
        self.__rgb.toggle()

    def toggle_amp(self):
        self.__amp.toggle()

    def __wait_until_boil(self, on_boil):
        temp = self.get_water_temp()
        while temp < 99:
            utils.sleep(5)
            temp = self.get_water_temp()
            print("Teapot's temp = " + str(temp))
        self.__teapot.off()
        on_boil()


# stub for running
#
#
# class Controller:
#
#     __led = "8d31a8"
#     __tea = False
#     __light = False
#
#     def __init__(self):
#         pass
#
#     def get_air_temp(self):
#         return 22.8
#
#     def get_water_temp(self):
#         return 70.1
#
#     def get_water_fullness(self):
#         return 80
#
#     def is_teapot_on(self):
#         return self.__tea
#
#     def is_light_on(self):
#         return self.__light
#
#     def set_led(self, color):
#         self.__led = color
#
#     def get_led_color(self):
#         return self.__led
#
#     def turn_on_teapot(self, on_boil):
#         self.__tea = True
#         threading.Thread(target=self.__boiling, args=(on_boil, )).start()
#
#     def toggle_light(self):
#         self.__light = not self.__light
#
#     def __boiling(self, on_boil):
#         start_time = utils.get_time()
#         while utils.get_time() - start_time < 10:
#             utils.sleep(1)
#         self.__tea = False
#         on_boil()
