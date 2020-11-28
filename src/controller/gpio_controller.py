from src.controller import Controller
import utils
import ds18b20

PIN_TEAPOT = 6
PIN_LIGHT = 14
PIN_AMP = 23

PIN_LED_R = 12
PIN_LED_G = 16
PIN_LED_B = 20

try:
    from gpiozero import RGBLED
except Exception as e:
    class RGBLED:
        value = (123, 123, 255)

        def __init__(self, _, __, ___):
            pass


class GpioController(Controller):

    # __teapot = None
    # __light = None
    # __amp = None
    # __temp_teapot = None
    __temp = None
    __led = None

    def __init__(self):
        # self.__teapot = DigitalOutputDevice(PIN_TEAPOT, active_high=False)
        # self.__light = DigitalOutputDevice(PIN_LIGHT, active_high=False)
        # self.__amp = DigitalOutputDevice(PIN_AMP, active_high=False)

        self.__temp = ds18b20.DS18B20()
        self.__led = RGBLED(PIN_LED_R, PIN_LED_G, PIN_LED_B)

    def get_temp(self) -> float:
        return self.__temp.get_ui_temp()

    def get_led_color(self) -> str:
        color = self.__led.value
        return hex(int(color[0] * 255))[2:].zfill(2) \
               + hex(int(color[1] * 255))[2:].zfill(2) \
               + hex(int(color[2] * 255))[2:].zfill(2)

    def set_led_color(self, color: str):
        curr_color = self.__led.value
        curr_r = curr_color[0]
        curr_g = curr_color[1]
        curr_b = curr_color[2]

        needed_r = int(color[:2], 16) / 255.0
        needed_g = int(color[2:4], 16) / 255.0
        needed_b = int(color[4:], 16) / 255.0

        duration = 500  # ms
        steps = int(60 * duration / 1000)
        for i in range(steps + 1):
            x = i / steps
            self.__led.color = (
                (needed_r - curr_r) * x + curr_r,
                (needed_g - curr_g) * x + curr_g,
                (needed_b - curr_b) * x + curr_b,
            )
            utils.sleep(.016)
