
TEA = "tea"
LIGHT = "light"
LED = "led"
LED_COLOR = "color"
PARROT = "parrot"
FUCK_YOU = "fy"
TEST = "test"
RGB = "rgb"
AMPLIFIER = "amp"


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
    # Action(
    #     "Teapot",
    #     TEA,
    #     "http://carnivalmunchies.com/wp-content/uploads/2015/09/tea.jpg",
    #     []
    # ),

    Action(
        "Light",
        LIGHT,
        "https://cdn.guidingtech.com/media/assets/WordPress-Import/2016/07/shutterstock_417763918.png",
        []
    ),

    # Action(
    #     "LED",
    #     LED,
    #     "https://upload.wikimedia.org/wikipedia/commons/c/cb/RBG-LED.jpg",
    #     [LED_COLOR]
    # ),
    #
    # Action(
    #     "Parrot",
    #     PARROT,
    #     "https://t2.ea.ltmcdn.com/en/images/4/1/0/img_names_of_famous_parrots_14_paso_1_600.jpg",
    #     []
    # ),
    #
    # Action(
    #     "Fuck You",
    #     FUCK_YOU,
    #     "https://i.imgur.com/O54cqIc.jpg",
    #     []
    # ),

    Action(
        "RGB",
        RGB,
        "https://sep.yimg.com/ay/yhst-135552442550403/24v-rgb-led-polar-2-neon-flex-65-1.jpg",
        []
    ),

    Action(
        "Amplifier",
        AMPLIFIER,
        "https://cdn.pixabay.com/photo/2016/03/31/15/24/audio-1293262_960_720.png",
        []
    ),

    Action(
        "Test",
        TEST,
        "https://www.webdevelopersnotes.com/wp-content/uploads/new-email-notification-sound-alert.png",
        []
    )
]


def get_action(action):
    for act in supported_actions:
        if act.action == action:
            return act
    return None
