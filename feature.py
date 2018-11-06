from enum import Enum


class Action(Enum):
    LIGHT = "light"
    RGB = "rgb"
    AMPLIFIER = "amp"


class Type(Enum):
    SWITCH = "switch"
    STATE = "state"
    SETTER = "setter"


class Feature:

    type = ""
    name = ""
    action = None
    params = None
    value = False

    def __init__(self, type, name, value, action=None, params=None):
        self.type = type
        self.name = name
        self.value = value
        self.action = action
        self.params = params

    def as_ui_obj(self):
        result = dict()
        result["type"] = self.type.value
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
            Type.SWITCH,
            "Light",
            ctrl.is_light_on(),
            Action.LIGHT
        ),
        Feature(
            Type.SWITCH,
            "RGB",
            ctrl.is_rgb_on(),
            Action.RGB
        ),
        Feature(
            Type.SWITCH,
            "Amplifier",
            ctrl.is_amp_on(),
            Action.AMPLIFIER
        )
    ]


def get_feature(action, features):
    for feature in features:
        if feature.action.value == action:
            return feature
    return None
