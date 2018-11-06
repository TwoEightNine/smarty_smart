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

    def __init__(self, name, value, action=None, params=None):
        self.name = name
        self.value = value
        self.action = action
        self.params = params

    def as_ui_obj(self):
        result = dict()
        result["name"] = self.name
        result["value"] = self.value
        if self.action is not None:
            result["action"] = self.action.value
        if self.params is not None:
            result["params"] = self.params
        return result


def build_features(ctrl):
    return [
        # switches
        Feature(
            "Light",
            on_off(ctrl.is_light_on()),
            Action.LIGHT
        ),
        Feature(
            "RGB",
            on_off(ctrl.is_rgb_on()),
            Action.RGB
        ),
        Feature(
            "Amplifier",
            on_off(ctrl.is_amp_on()),
            Action.AMPLIFIER
        )
    ]


def on_off(value):
    return "ON" if value else "OFF"


def get_feature(action, features):
    for feature in features:
        if feature.action.value == action:
            return feature
    return None
