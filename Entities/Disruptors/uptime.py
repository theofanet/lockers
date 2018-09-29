from Entities.Disruptors.disruptor import *


class Uptime(Disruptor):

    def __init__(self, img):
        super().__init__(img)

    @staticmethod
    def trigger_effect(elapsed_time):
        updated_timer = elapsed_time - 10000
        if updated_timer > 0:
            return updated_timer
        return 0
