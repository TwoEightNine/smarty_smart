from abc import abstractmethod, ABC


class Controller(ABC):

    @abstractmethod
    def get_temp(self) -> float:
        pass

    @abstractmethod
    def get_led_color(self) -> str:
        pass

    @abstractmethod
    def set_led_color(self, color: str):
        pass
