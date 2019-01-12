import badge
import ugfx
import time
import appglue
import _thread


class Strobonator:
    def __init__(self):
        self.strobonator_on = True
        self.delay = 50.0
        _thread.start_new_thread(self.run, ())

    def run(self):
        latch = False
        while True:
            if latch or self.strobonator_on == False:
                badge.backlight(0)
                badge.led(6, 0, 0, 0)
                latch = False
            else:
                badge.backlight(255)
                badge.led(6, 255, 255, 255)
                latch = True
            time.sleep(self.delay / 1000)

    def press_start(self, button_pressed):
        if button_pressed:
            if self.strobonator_on:
                self.strobonator_on = False
            else:
                self.strobonator_on = True

    def press_down(self, button_pressed):
        if self.delay > 10 and button_pressed:
            self.delay -= 10

    def press_up(self, button_pressed):
        if self.delay < 1000 and button_pressed:
            self.delay += 10


def main():
    strobonator = Strobonator()
    ugfx.input_attach(ugfx.BTN_START, strobonator.press_start)
    ugfx.input_attach(ugfx.JOY_UP, strobonator.press_up)
    ugfx.input_attach(ugfx.JOY_DOWN, strobonator.press_down)


ugfx.input_init()
ugfx.input_attach(ugfx.BTN_B, lambda pushed: appglue.home()
                  if pushed else False)

_thread.start_new_thread(main, ())
