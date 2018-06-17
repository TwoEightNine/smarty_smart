class Action:

    name = ""
    action = ""
    thumb = ""
    params = []

    def __init__(self, name, action, thumb, params):
        self.name = name
        self.action = action
        self.thumb = thumb
        self.params = params

    def as_ui_obj(self):
        return {
            "name": self.name,
            "action": self.action,
            "thumb": self.thumb,
            "params": self.params
        }


supported_actions = [
        Action("Teapot", "tea", "", []).as_ui_obj(),
        Action("Light", "light", "", []).as_ui_obj(),
        Action("LED", "led", "", ["color"]).as_ui_obj(),
        Action("Fuck You", "fy", "", []).as_ui_obj()
    ]


def get_action(action):
    for act in supported_actions:
        if act["action"] == action:
            return act
    return None
