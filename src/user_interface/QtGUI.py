from AbstractGUI import AbstractGUI


class QtGUI(AbstractGUI):
    def __init__(self):
        super().__init__()

    def mainloop(self):
        observation = self.get_observation()
