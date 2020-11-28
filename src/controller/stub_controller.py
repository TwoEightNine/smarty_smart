from src.controller import Controller


class StubController(Controller):

    __led_color = "7d7dff"

    def get_temp(self) -> float:
        return 22.8

    def get_led_color(self) -> str:
        return self.__led_color

    def set_led_color(self, color: str):
        self.__led_color = color
