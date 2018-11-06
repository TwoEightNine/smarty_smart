from enum import Enum


class Action(Enum):
    LIGHT = "light"
    RGB = "rgb"
    AMPLIFIER = "amp"


class Feature:

    name = ""
    action = None
    params = None
    value = ""
    thumb = None

    def __init__(self, name, value, action=None, params=None, thumb=None):
        self.name = name
        self.value = value
        self.action = action
        self.params = params
        self.thumb = thumb

    def as_ui_obj(self):
        result = dict()
        result["name"] = self.name
        result["value"] = self.value
        if self.action is not None:
            result["action"] = self.action.value
        if self.params is not None:
            result["params"] = self.params
        if self.thumb is not None:
            result["thumb"] = self.thumb
        return result


def build_features(ctrl):
    return [
        Feature(
            "Air temp, °C",
            str(ctrl.get_air_temp()),
            thumb="http://www.cray.com/blog/wp-content/uploads/2015/09/Weather-Blog-Image.jpg"
        ),
        Feature(
            "Light",
            on_off(ctrl.is_light_on()),
            Action.LIGHT,
            thumb="https://cdn.guidingtech.com/media/assets/WordPress-Import/2016/07/shutterstock_417763918.png"
        ),
        Feature(
            "RGB",
            on_off(ctrl.is_rgb_on()),
            Action.RGB,
            thumb="https://sep.yimg.com/ay/yhst-135552442550403/24v-rgb-led-polar-2-neon-flex-65-1.jpg"
        ),
        Feature(
            "Amplifier",
            on_off(ctrl.is_amp_on()),
            Action.AMPLIFIER,
            thumb="https://cdn.pixabay.com/photo/2016/03/31/15/24/audio-1293262_960_720.png"
        )
    ]


def on_off(value):
    return "ON" if value else "OFF"


def get_feature(action, features):
    for feature in features:
        if feature.action is not None and \
                feature.action.value == action:
            return feature
    return None
