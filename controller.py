# from gpiozero import DigitalOutputDevice, RGBLED
import ds18b20

PIN_TEAPOT = 6
PIN_LIGHT = 7
PIN_LED_R = 13
PIN_LED_G = 14
PIN_LED_B = 15


# class Controller:
#
#     __teapot = None
#     __light = None
#     __temp_teapot = None
#     __temp_air = None
#     __led = None
#
#     def __init__(self):
#         self.__teapot = DigitalOutputDevice(PIN_TEAPOT)
#         self.__light = DigitalOutputDevice(PIN_LIGHT)
#         self.__temp_teapot = ds18b20.DS18B20()
#         self.__temp_air = ds18b20.DS18B20()
#         self.__led = RGBLED(PIN_LED_R, PIN_LED_G, PIN_LED_B)
#         pass
#
#     def get_air_temp(self):
#         return self.__temp_air.get_temp()
#
#     def get_water_temp(self):
#         return self.__temp_teapot.get_temp()
#
#     def get_water_fullness(self):
#         return 80
#
#     def is_teapot_on(self):
#         return self.__teapot.value
#
#     def is_light_on(self):
#         return self.__light.value
#
#     def set_led(self, color):
#         self.__led.color = (
#             int(color[:2], 16) / 255.0,
#             int(color[2:4], 16) / 255.0,
#             int(color[4:], 16) / 255.0
#         )
#
#     def get_led_color(self):
#         color = self.__led.value
#         return hex(int(color[0] * 255))[2:] \
#                + hex(int(color[1] * 255))[2:] \
#                + hex(int(color[2] * 255))[2:]
#
#     def turn_on_teapot(self):
#         self.__teapot.on()
#
#     def toggle_light(self):
#         self.__light.toggle()


# stub for running
#
#
class Controller:

    __led = "8d31a8"
    __tea = False
    __light = False

    def __init__(self):
        pass

    def get_air_temp(self):
        return 22.8

    def get_water_temp(self):
        return 70.1

    def get_water_fullness(self):
        return 80

    def is_teapot_on(self):
        return self.__tea

    def is_light_on(self):
        return self.__light

    def set_led(self, color):
        self.__led = color

    def get_led_color(self):
        return self.__led

    def turn_on_teapot(self):
        self.__tea = not self.__tea

    def toggle_light(self):
        self.__light = not self.__light
