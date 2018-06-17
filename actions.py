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
        Action("Teapot", "tea", "http://carnivalmunchies.com/wp-content/uploads/2015/09/tea.jpg", []).as_ui_obj(),
        Action("Light", "light", "https://cdn.guidingtech.com/media/assets/WordPress-Import/2016/07/shutterstock_417763918.png", []).as_ui_obj(),
        Action("LED", "led", "https://upload.wikimedia.org/wikipedia/commons/c/cb/RBG-LED.jpg", ["color"]).as_ui_obj(),
        Action("Fuck You", "fy", "https://i.imgur.com/O54cqIc.jpg", []).as_ui_obj()
    ]


def get_action(action):
    for act in supported_actions:
        if act["action"] == action:
            return act
    return None
