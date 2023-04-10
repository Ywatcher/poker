# -*- coding: utf-8 -*-
from enum import Enum


class Event:
    class Type(Enum):
        updateObs = 0
        updateHistory = 1

    def __init__(self, event_type: "Event.Type", **kwargs):
        self.type = event_type
        self.param = kwargs
        # print(kwargs)


# if __name__ == "__main__":
    # e = Event(type=Event.Type.updateObs, a=0, b=1)
